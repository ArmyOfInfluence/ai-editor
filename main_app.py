import pyperclip
import streamlit as st
import io
import datetime
from constants import OPENAI_API_KEY, ASSISTANTS, OPENAI_MODEL
from assistant_manager import AssistantManager
from markdown_converter import convert_to_markdown, markdown_converter_ui
import ui_components
import utils

class StreamlitApp:
    def __init__(self):
        self.assistant_manager = AssistantManager(OPENAI_API_KEY, OPENAI_MODEL)

    def run(self):
        self.setup_page()
        self.initialize_session_state()
        self.create_sidebar()

        if st.session_state.current_page == "Home":
            self.render_home_page()
        elif st.session_state.current_page == "History":
            self.render_history_page()

    def initialize_session_state(self):
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

    def setup_page(self):
        st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

    def create_sidebar(self):
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
    
    def render_instagram_options(self):
        st.session_state.show_instagram_options = st.toggle("Show Instagram Content Options", value=st.session_state.show_instagram_options)
        
        if st.session_state.show_instagram_options:
            st.subheader("Instagram Content Options")
            st.session_state.num_slides = st.number_input("Number of slides:", min_value=1, max_value=10, value=st.session_state.num_slides)
            st.session_state.chars_per_slide = st.number_input("Characters per slide:", min_value=50, max_value=500, value=st.session_state.chars_per_slide)
        else:
            st.info("Instagram content settings will be determined by the AI.")
    
    def render_home_page(self):
        st.title("🤖 AI Editor in Chief")
        st.caption("🇺🇦 Powered by UActuality")

        user_input = ui_components.create_text_input(key="user_input")
        
        tabs = ui_components.create_assistant_tabs(ASSISTANTS)

        for i, tab in enumerate(tabs[:-1]):
            with tab:
                st.write(f"Using the {ASSISTANTS[i]['name']} assistant.")

                if ASSISTANTS[i]['name'] == "Build Instagram Content":
                    self.render_instagram_options()

                if ui_components.create_process_button(ASSISTANTS[i]['name'], key=f"process_button_{i}"):
                    if user_input:
                        response = self.handle_user_input(user_input, ASSISTANTS[i]['id'])
                        self.display_assistant_response(response)
                    else:
                        ui_components.create_warning_message("Please enter some text before processing.", key=f"warning_{i}")

        with tabs[-1]:
            markdown_converter_ui(user_input)

    def render_history_page(self):
        st.title("Conversation History")
        for index, msg in enumerate(st.session_state.messages):
            formatted_message = utils.format_message_for_display(msg)
            if msg['role'] == 'user':
                st.text_area(f"User (Message {index}):", formatted_message, height=100, disabled=True)
            else:
                st.markdown(formatted_message)
                self.create_message_actions(msg, index)
            st.markdown("---")

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

        st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})

        if st.session_state.thread is None:
            st.session_state.thread = self.assistant_manager.create_thread()

        self.assistant_manager.add_message_to_thread(st.session_state.thread, "user", cleaned_input)
        
        with ui_components.create_spinner("Processing your input..."):
            self.assistant_manager.run_assistant(st.session_state.thread, assistant_id)

        response = self.assistant_manager.get_assistant_response(st.session_state.thread)
        st.session_state.messages.append({"role": "assistant", "content": response, "timestamp": timestamp})
        return response

    def display_assistant_response(self, response):
        st.subheader("Assistant Response:")
        st.markdown(response)
        st.caption(f"Word count: {utils.count_words(response)}")
        self.create_message_actions({"content": response, "timestamp": datetime.datetime.now().strftime("%Y%m%d%H%M%S")}, len(st.session_state.messages) - 1)

    def create_message_actions(self, msg, index):
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
            self.create_download_button(msg, index)
        
        with col3:
            if ui_components.create_clear_button("Clear Result", key=f"clear_button_{index}"):
                st.session_state[f"response_area_{index}"] = ""
                st.experimental_rerun()
        
        # Display success message if copy was successful
        if st.session_state.get(f"copy_success_{index}", False):
            st.success("Copied to clipboard as Markdown!")
            st.code(convert_to_markdown(content), language="markdown")
            # Reset the success flag
            st.session_state[f"copy_success_{index}"] = False

    def create_download_button(self, msg, index):
        markdown_content = convert_to_markdown(st.session_state[f"response_area_{index}"])
        message_bytes = markdown_content.encode('utf-8')
        message_buffer = io.BytesIO(message_bytes)
        ui_components.create_download_button(
            label="Download as Markdown",
            data=message_buffer,
            file_name=f"assistant_response_{msg.get('timestamp', index)}.md",
            key=f"download_button_{index}"
        )