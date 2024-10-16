import streamlit as st
import datetime
from constants import OPENAI_API_KEY, OPENAI_MODEL, ASSISTANTS
from assistant_manager import AssistantManager
from pages import HomePage, HistoryPage
from ui_manager import UIManager
from state_manager import StateManager
import utils
from file_utils import parse_uploaded_file

class StreamlitApp:
    def __init__(self):
        self.assistant_manager = AssistantManager(OPENAI_API_KEY, OPENAI_MODEL)
        self.home_page = HomePage(self)
        self.history_page = HistoryPage(self)
        self.ui_manager = UIManager()

    def run(self):
        self.setup_page()
        StateManager.initialize_session_state()
        self.ui_manager.create_sidebar()

        if st.session_state.current_page == "Home":
            self.home_page.render()
        elif st.session_state.current_page == "History":
            self.history_page.render()

    def setup_page(self):
        st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

    def handle_user_input(self, user_input, assistant_id):
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        assistant_name = next((a['name'] for a in ASSISTANTS if a['id'] == assistant_id), None)
        if assistant_name == "Build Instagram Content":
            cleaned_input = f"\n\n{{ARTICLE_TEXT}}: {utils.clean_text(user_input)}"

            if st.session_state.show_instagram_options:
                cleaned_input += f"\n\n{{NUM_SLIDES}}: {st.session_state.num_slides}"
                cleaned_input += f"\n{{CHARS_PER_SLIDE}}: {st.session_state.chars_per_slide}"
        else:
            cleaned_input = utils.clean_text(user_input)

        StateManager.add_message("user", user_input, timestamp)

        if StateManager.get_thread() is None:
            StateManager.set_thread(self.assistant_manager.create_thread())

        self.assistant_manager.add_message_to_thread(StateManager.get_thread(), "user", cleaned_input)
        
        with st.spinner("Processing your input..."):
            self.assistant_manager.run_assistant(StateManager.get_thread(), assistant_id)

        response = self.assistant_manager.get_assistant_response(StateManager.get_thread())
        StateManager.add_message("assistant", response, timestamp)
        return response

    def display_assistant_response(self, response):
        self.ui_manager.display_assistant_response(response)
        self.ui_manager.create_message_actions({"content": response, "timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S")}, len(st.session_state.messages) - 1)

    def create_message_actions(self, msg, index):
        self.ui_manager.create_message_actions(msg, index)

    def handle_file_upload(self):
        uploaded_file = st.file_uploader("Choose a file", type=['md', 'pdf', 'txt'])
        if uploaded_file is not None:
            try:
                file_content = parse_uploaded_file(uploaded_file)
                st.session_state.user_input = file_content
                st.success(f"File '{uploaded_file.name}' uploaded and parsed successfully!")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")