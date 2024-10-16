import io
import pyperclip
import streamlit as st
from markdown_converter import convert_to_markdown
import ui_components
import utils

class UIManager:
    @staticmethod
    def create_sidebar():
        with st.sidebar:
            st.title("Navigation")
            
            if ui_components.create_sidebar_button("Home", key="home"):
                st.session_state.current_page = "Home"
            
            if ui_components.create_sidebar_button("Conversation History", key="history"):
                st.session_state.current_page = "History"
            
            st.title("Recent Conversations")
            
            for i, msg in enumerate(reversed(st.session_state.messages[-10:])):
                if msg['role'] == 'user':
                    title = utils.truncate_text(msg['content'], max_length=50)
                    
                    if ui_components.create_sidebar_button(title, key=f"sidebar_msg_{i}"):
                        st.session_state.current_page = "History"
                        st.session_state.selected_message_index = len(st.session_state.messages) - i - 1
            
            if ui_components.create_sidebar_button("Clear All Conversations", key="clear_conversations"):
                st.session_state.messages = []
                st.session_state.thread = None
                st.rerun()
            
            st.sidebar.markdown("---")
            st.sidebar.caption("AI Assistant v1.0")
            st.sidebar.caption("© 2024 Build with ♥️ by UActuality team 🇺🇦")

    @staticmethod
    def display_assistant_response(response):
        st.subheader("Assistant Response:")
        st.markdown(response)
        st.caption(f"Word count: {utils.count_words(response)}")

    @staticmethod
    def create_message_actions(msg, index):
        if f"response_area_{index}" not in st.session_state:
            st.session_state[f"response_area_{index}"] = msg['content']
        
        content = st.text_area(f"Response {index}", 
                            value=st.session_state[f"response_area_{index}"], 
                            height=200, 
                            key=f"response_area_{index}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Copy as Markdown", key=f"copy_button_{index}"):
                markdown_content = convert_to_markdown(content)
                pyperclip.copy(markdown_content)
                st.session_state[f"copy_success_{index}"] = True
        
        with col2:
            UIManager.create_download_button(msg, index)
        
        with col3:
            if ui_components.create_clear_button("Clear Result", key=f"clear_button_{index}"):
                st.session_state[f"response_area_{index}"] = ""
                st.experimental_rerun()
        
        if st.session_state.get(f"copy_success_{index}", False):
            st.success("Copied to clipboard as Markdown!")
            st.code(convert_to_markdown(content), language="markdown")
            st.session_state[f"copy_success_{index}"] = False

    @staticmethod
    def create_download_button(msg, index):
        markdown_content = convert_to_markdown(st.session_state[f"response_area_{index}"])
        message_bytes = markdown_content.encode('utf-8')
        message_buffer = io.BytesIO(message_bytes)
        ui_components.create_download_button(
            label="Download as Markdown",
            data=message_buffer,
            file_name=f"assistant_response_{msg.get('timestamp', index)}.md",
            key=f"download_button_{index}"
        )