import streamlit as st
import requests
import uuid

st.set_page_config(page_title="Agentic RAG", layout="wide")
st.title("Agentic RAG System")

API_URL = "http://localhost:8000"

# --- Session Management ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
    
st.sidebar.text(f"Session ID:\n{st.session_state.session_id}")

# --- Sidebar: Ingestion ---
with st.sidebar:
    st.header("Knowledge Base")
    uploaded_file = st.file_uploader("Upload Document", type=["pdf", "txt", "md", "docx"])
    
    if uploaded_file is not None:
        if st.button("Ingest Document"):
            with st.spinner("Ingesting..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    response = requests.post(f"{API_URL}/ingest", files=files)
                    if response.status_code == 200:
                        st.success("Ingestion Successful!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- Main Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
prompt = st.chat_input("Ask a question (e.g., 'Find info about X and search web for Y')")

if prompt:
    # 1. Add User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call Backend
    with st.chat_message("assistant"):
        placeholder = st.empty()
        with st.spinner("Agent is thinking..."):
            try:
                payload = {
                    "query": prompt,
                    "thread_id": st.session_state.session_id
                }
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display Final Answer
                    answer = data.get("answer", "No answer generated.")
                    placeholder.markdown(answer)
                    
                    # Update History
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                    
                    # Display Agent Thoughts (Plan & Execution)
                    with st.expander("View Agent Reasoning & Steps", expanded=False):
                        st.subheader("Planning")
                        plan = data.get("plan", [])
                        if plan:
                            for i, step in enumerate(plan):
                                st.write(f"**Step {i+1}**: {step.get('reasoning')} ({step.get('tool')})")
                        else:
                            st.warning("No plan returned.")

                        st.subheader("Execution Trace")
                        details = data.get("execution_details", [])
                        for i, res in enumerate(details):
                            st.markdown(f"**Result {i+1}**")
                            st.caption(f"Tool: {res.get('step', {}).get('tool')}")
                            st.code(res.get('output'), language=None)
                            
                else:
                    placeholder.error(f"Backend Error: {response.status_code} - {response.text}")
            except Exception as e:
                placeholder.error(f"Connection Failed: {e}")
