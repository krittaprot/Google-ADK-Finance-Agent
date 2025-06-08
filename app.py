import streamlit as st
import requests
import json
import os
import uuid
import time

st.title("Finance Agent")

# --- Helper function to escape dollar signs for Streamlit ---
def escape_markdown_dollars(text: str) -> str:
    """
    Replaces all standalone dollar signs with a backslash-escaped
    version to prevent Streamlit from interpreting them as LaTeX.
    """
    if isinstance(text, str):
        return text.replace('$', '\\$')
    return text

# Initialize chat history and other session variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = f"user-{uuid.uuid4()}"
    
if "session_id" not in st.session_state:
    st.session_state.session_id = None

# User input for agent URL and name
st.sidebar.header("Agent Configuration")
agent_url = st.sidebar.text_input("ADK Agent API URL", "http://localhost:8000")
agent_name = st.sidebar.text_input("Agent Name (e.g., finance_agent)", "finance_agent")

def create_session(agent_url, agent_name, user_id):
    """
    Create a new session with the specified agent.
    """
    session_id = f"session-{int(time.time())}"
    session_init_url = f"{agent_url}/apps/{agent_name}/users/{user_id}/sessions/{session_id}"
    try:
        response = requests.post(session_init_url, headers={"Content-Type": "application/json"}, json={"state": {}})
        response.raise_for_status()
        st.session_state.session_id = session_id
        st.session_state.messages = []
        st.success(f"New session created: {session_id}")
        st.rerun() # Rerun to update the UI immediately
        return True
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Failed to initiate session: {e}")
        return False

# Sidebar for session management
with st.sidebar:
    st.header("Session Management")
    if st.session_state.session_id:
        st.success(f"Active session: {st.session_state.session_id}")
        if st.button("➕ New Session"):
            create_session(agent_url, agent_name, st.session_state.user_id)
    else:
        st.warning("No active session.")
        if st.button("➕ Create Session"):
            create_session(agent_url, agent_name, st.session_state.user_id)

st.divider()

def send_message(message, agent_url, agent_name):
    """
    Sends a message to the agent and renders the response in a structured, streaming way.
    Tool calls are displayed using st.status in chronological order.
    """
    if not st.session_state.session_id:
        st.error("No active session. Please create a session first.")
        return

    # Add user message to chat history immediately for a responsive feel
    st.session_state.messages.append({"role": "user", "content": message})

    # Display the user's message in the chat
    with st.chat_message("user"):
        st.markdown(message)

    # Prepare payload for ADK agent API
    payload = {
        "appName": agent_name,
        "userId": st.session_state.user_id,
        "sessionId": st.session_state.session_id,
        "newMessage": {"role": "user", "parts": [{"text": message}]},
        "streaming": True,
    }
    headers = {"Content-Type": "application/json"}
    full_url = f"{agent_url}/run_sse"

    # This will hold the final, user-facing text response from the LLM
    final_response_text = ""
    
    # Dictionary to track tool calls by their ID
    tool_containers = {}
    
    # Create the assistant chat message container FIRST
    with st.chat_message("assistant"):
        # This will hold all the content within the assistant message
        assistant_container = st.container()
        
        # Placeholder for the final text response
        final_text_placeholder = st.empty()

        try:
            with requests.post(full_url, headers=headers, json=payload, stream=True) as response:
                response.raise_for_status()
                for chunk in response.iter_content(chunk_size=None):
                    if not chunk:
                        continue
                    try:
                        lines = chunk.decode('utf-8').splitlines()
                        for line in lines:
                            if not line.startswith("data:"):
                                continue
                            
                            json_data = line[len("data:"):].strip()
                            if not json_data:  # Skip empty data lines
                                continue
                                
                            event = json.loads(json_data)

                            # Check if this event has content and parts
                            if "content" in event and event["content"].get("parts"):
                                for part in event["content"]["parts"]:
                                    # Handle function calls (tool execution start)
                                    if "functionCall" in part:
                                        tool_id = part["functionCall"]["id"]
                                        tool_name = part["functionCall"]["name"]
                                        tool_args = part["functionCall"]["args"]
                                        
                                        with assistant_container:
                                            status_container = st.status(f"Executing tool: `{tool_name}`...", state="running")
                                            with status_container:
                                                st.json(tool_args)
                                        
                                        tool_containers[tool_id] = status_container
                                    
                                    # Handle function responses (tool execution results)
                                    elif "functionResponse" in part:
                                        tool_id = part["functionResponse"]["id"]
                                        tool_name = part["functionResponse"]["name"]
                                        tool_result = part["functionResponse"]["response"]
                                        
                                        if tool_id in tool_containers:
                                            status_container = tool_containers[tool_id]
                                            with status_container:
                                                st.markdown("**Result:**")
                                                st.json(tool_result)
                                            status_container.update(state="complete")
                                            del tool_containers[tool_id]
                                    
                                    # Handle text responses (final LLM response)
                                    elif "text" in part:
                                        text_content = part["text"]
                                        is_partial = event.get("partial", True)

                                        # ---- FIX FOR DUPLICATION IS HERE ----
                                        # If the message is partial, append it (streaming).
                                        # If it's not partial, it's the final complete message, so replace the text.
                                        if is_partial:
                                            final_response_text += text_content
                                        else:
                                            final_response_text = text_content
                                        
                                        # Update the final text placeholder with the escaped text
                                        final_text_placeholder.markdown(escape_markdown_dollars(final_response_text) + "▌")
                                    
                    except json.JSONDecodeError as e:
                        print(f"Could not decode JSON: {line} - Error: {e}")
                    except Exception as e:
                        print(f"Error processing chunk: {e}")

            # Final update - remove the blinking cursor
            if final_response_text:
                final_text_placeholder.markdown(escape_markdown_dollars(final_response_text))
            else:
                # If no text response was received, show a placeholder
                final_text_placeholder.markdown("*Response completed*")

        except requests.exceptions.RequestException as e:
            error_message = f"Error connecting to agent: {e}"
            final_text_placeholder.error(error_message)
            final_response_text = error_message
        except Exception as e:
            error_message = f"An unexpected error occurred: {e}"
            final_text_placeholder.error(error_message)
            final_response_text = error_message

    # Save the clean, final text to the session state
    st.session_state.messages.append({"role": "assistant", "content": final_response_text})

# Display all messages from chat history on app rerun
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(escape_markdown_dollars(msg["content"]))

# Input for new messages
if st.session_state.session_id:  # Only show input if a session exists
    if user_input := st.chat_input("Ask about a stock..."):
        send_message(user_input, agent_url, agent_name)
else:
    st.info("👈 Create a session to start chatting")