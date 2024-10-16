import streamlit as st
import ui_components
import utils
from constants import ASSISTANTS

class HomePage:
    def __init__(self, app):
        self.app = app

    def render(self):
        st.title("🤖 AI Editor in Chief")
        st.caption("🇺🇦 Powered by UActuality")

        self.app.handle_file_upload()

        if 'user_input' not in st.session_state:
            st.session_state.user_input = ''

        user_input = ui_components.create_text_input(key="user_input")
        
        if user_input != st.session_state.user_input:
            st.session_state.user_input = user_input

        tabs = ui_components.create_assistant_tabs(ASSISTANTS)

        for i, tab in enumerate(tabs[:-1]):
            with tab:
                st.write(f"Using the {ASSISTANTS[i]['name']} assistant.")

                if ASSISTANTS[i]['name'] == "Build Instagram Content":
                    self.render_instagram_options()

                if ui_components.create_process_button(ASSISTANTS[i]['name'], key=f"process_button_{i}"):
                    if st.session_state.user_input:
                        response = self.app.handle_user_input(st.session_state.user_input, ASSISTANTS[i]['id'])
                        self.app.display_assistant_response(response)
                    else:
                        ui_components.create_warning_message("Please enter some text or upload a file before processing.", key=f"warning_{i}")

    def render_instagram_options(self):
        st.session_state.show_instagram_options = st.toggle("Show Instagram Content Options", value=st.session_state.show_instagram_options)
        
        if st.session_state.show_instagram_options:
            st.subheader("Instagram Content Options")
            st.session_state.num_slides = st.number_input("Number of slides:", min_value=1, max_value=10, value=st.session_state.num_slides)
            st.session_state.chars_per_slide = st.number_input("Characters per slide:", min_value=50, max_value=500, value=st.session_state.chars_per_slide)
        else:
            st.info("Instagram content settings will be determined by the AI.")

class HistoryPage:
    def __init__(self, app):
        self.app = app

    def render(self):
        st.title("Conversation History")
        for index, msg in enumerate(st.session_state.messages):
            formatted_message = utils.format_message_for_display(msg)
            if msg['role'] == 'user':
                st.text_area(f"User (Message {index}):", formatted_message, height=100, disabled=True)
            else:
                st.markdown(formatted_message)
                self.app.create_message_actions(msg, index)
            st.markdown("---")