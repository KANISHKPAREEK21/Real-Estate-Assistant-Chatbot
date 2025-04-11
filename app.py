import streamlit as st
import uuid
from openai import OpenAI
from function_helper import createThread, call_stream_assistant, handle_file_upload, delete_assistant_file
import os
from dotenv import load_dotenv
load_dotenv()

# Setup
GPT_API_KEY = os.getenv("OPENAI_API_KEY")
OpenAIclient = OpenAI(api_key=GPT_API_KEY)

st.set_page_config(page_title="Real Estate Chatbot", layout="wide")

# ---- Session Initialization ---- #
if 'chat_sessions' not in st.session_state:
    st.session_state.chat_sessions = {}
if 'selected_session' not in st.session_state:
    st.session_state.selected_session = None

# Only create a new thread on first load if no sessions exist
if not st.session_state.chat_sessions:
    thread_id = createThread()
    st.session_state.chat_sessions[thread_id] = []
    st.session_state.selected_session = thread_id
    delete_assistant_file()

# ---- Sidebar: Chat History & New Chat ---- #
st.sidebar.title("Chat History")

session_list = []
session_labels = []

# Build labeled chat history with previews
for thread_id, messages in st.session_state.chat_sessions.items():
    if messages:
        preview = messages[-1]['content']
        preview = preview[:30] + "..." if len(preview) > 30 else preview
    else:
        preview = "New Chat"
    session_list.append(thread_id)
    session_labels.append(preview)

# Display selectbox with previews
if session_labels:
    selected_label = st.sidebar.selectbox("Select a session", session_labels)
    selected_index = session_labels.index(selected_label)
    st.session_state.selected_session = session_list[selected_index]

# "Start New Chat" button in sidebar
if st.sidebar.button("Start New Chat"):
    thread_id = createThread()
    st.session_state.chat_sessions[thread_id] = []
    st.session_state.selected_session = thread_id
    delete_assistant_file()
    st.rerun()  # Refresh to clear input + view new thread

# ---- Main Chat Interface ---- #
st.title("Real Estate Assistant Chatbot")

# Get current thread
thread = st.session_state.selected_session
chat_history = st.session_state.chat_sessions.get(thread, [])

# Scrollable chat area using a container
chat_placeholder = st.container()

with chat_placeholder:
    for msg in chat_history:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        else:
            st.chat_message("assistant").markdown(msg["content"])

with st.form("chat_form", clear_on_submit=True):
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
    user_input = st.text_input("Your message:")
    submitted = st.form_submit_button("➤")



# ---- Message Handling ---- #
if submitted:
    # Image upload handling
    if uploaded_image:
        file_path = handle_file_upload(uploaded_image)
        st.image(uploaded_image, caption="Uploaded Image", use_container_width=False)
        st.success("Image uploaded and linked to assistant.")

    # Text message handling
    if user_input:
        st.session_state.chat_sessions[thread].append({"role": "user", "content": user_input})

    # Choose message to query
    query_msg = user_input if user_input else None
    response = call_stream_assistant(msg=query_msg, Thread_ID=thread)

    # Stream assistant response
    assistant_message = ""
    with st.chat_message("assistant"):
        assistant_box = st.empty()
        for event in response:
            if event.data.object == 'thread.message.delta':
                for content in event.data.delta.content:
                    if hasattr(content, "text"):
                        chunk = content.text.value
                        assistant_message += chunk
                        html_content = assistant_message.replace("\n", "<br>")
                        assistant_box.markdown(f"<b>Assistant:</b><br>{html_content}", unsafe_allow_html=True)
                    elif hasattr(content, "image_url"):  # or whatever the attribute is
                        print("Image URL:", content.image_url.url)
                        assistant_box.markdown(content.image_url.url)

    st.session_state.chat_sessions[thread].append({"role": "assistant", "content": assistant_message})
