# File: ui_components.py

import streamlit as st

def create_text_input(key="user_input", height=200):
    """Create the main text input area."""
    return st.text_area("Enter your text here:", height=height, key=key)

def create_assistant_tabs(assistants):
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        border-radius: 10px 10px 0 0;
        font-size: 16px;
        font-weight: 500;
        color: #FFFFFF;
    }
    .stTabs [data-baseweb="tab"]:nth-child(1) { background-color: #FF6B6B; }
    .stTabs [data-baseweb="tab"]:nth-child(2) { background-color: #4ECDC4; }
    .stTabs [data-baseweb="tab"]:nth-child(3) { background-color: #8A2BE2; }
    .stTabs [data-baseweb="tab"]:nth-child(4) { background-color: #F7B801; }
    .stTabs [aria-selected="true"] {
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    # Create tabs
    tabs = st.tabs([assistant['name'] for assistant in assistants] + ["Markdown Converter"])
    
    return tabs

def create_process_button(assistant_name, key):
    """Create a process button for an assistant."""
    return st.button(f"Process with {assistant_name}", key=key)

def create_copy_button(label, key):
    """Create a button to copy content."""
    return st.button(label, key=key)

def create_message_box(role, content, is_user=False, key=None):
    """Create a message box for displaying messages."""
    if is_user:
        return st.text_area(f"{role}:", value=content, height=100, disabled=True, key=key)
    else:
        with st.expander(f"{role} Response", expanded=True):
            st.markdown(content, key=key)

def create_sidebar_button(label, key):
    """Create a button for the sidebar."""
    return st.sidebar.button(label, key=key)

def create_sidebar_recent_conversations(messages, max_conversations=10):
    """Create buttons for recent conversations in the sidebar."""
    st.sidebar.title("Recent Conversations")
    for i, msg in enumerate(messages[-max_conversations:]):
        if msg['role'] == 'user':
            title = ' '.join(msg['content'].split()[:3]) + '...'  # First 3 words
            if st.sidebar.button(title, key=f"sidebar_msg_{i}"):
                return i  # Return index if button is clicked
    return None

def create_markdown_preview(markdown_text, key):
    """Create a preview of markdown text."""
    st.subheader("Markdown Preview:")
    st.markdown(markdown_text, key=key)

def create_success_message(message, key):
    """Create a success message."""
    st.success(message, key=key)

def create_warning_message(message, key):
    """Create a warning message."""
    st.warning(message, key=key)

def create_info_message(message, key):
    """Create an info message."""
    st.info(message, key=key)

def create_error_message(message, key):
    """Create an error message."""
    st.error(message, key=key)

def create_spinner(message):
    """Create a spinner with a message."""
    return st.spinner(message)

def create_file_uploader(label, type, key):
    """Create a file uploader."""
    return st.file_uploader(label, type=type, key=key)

def create_download_button(label, data, file_name, key):
    """Create a download button."""
    return st.download_button(label=label, data=data, file_name=file_name, key=key)

def create_clear_button(label, key):
    """Create a button to clear content."""
    return st.button(label, key=key)