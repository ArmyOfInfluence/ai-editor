import streamlit as st

class StateManager:
    @staticmethod
    def initialize_session_state():
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "thread" not in st.session_state:
            st.session_state.thread = None
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Home"
        if "show_instagram_options" not in st.session_state:
            st.session_state.show_instagram_options = False
        if "num_slides" not in st.session_state:
            st.session_state.num_slides = 7
        if "chars_per_slide" not in st.session_state:
            st.session_state.chars_per_slide = 280

    @staticmethod
    def add_message(role, content, timestamp):
        st.session_state.messages.append({"role": role, "content": content, "timestamp": timestamp})

    @staticmethod
    def clear_conversations():
        st.session_state.messages = []
        st.session_state.thread = None

    @staticmethod
    def set_thread(thread_id):
        st.session_state.thread = thread_id

    @staticmethod
    def get_thread():
        return st.session_state.thread