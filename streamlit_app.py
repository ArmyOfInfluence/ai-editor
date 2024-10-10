from openai import OpenAI
import streamlit as st

from constants import OPENAI_API_KEY, OPENAI_ASSISTANT_ID, OPENAI_MODEL

st.title("✍️ AI Editor")
st.caption("🇺🇦 Article editor powered by UActuality")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "I'm your AI Editor. Please enter your article in markdown format below."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Add markdown input area
markdown_input = st.text_area("Enter your article in markdown format:", "")

if st.button("Preview Markdown"):
    if markdown_input:
        st.subheader("Markdown Preview:")
        st.markdown(markdown_input)
    else:
        st.warning("Please enter some text to preview.")

if st.button("Submit Article"):
    if not markdown_input:
        st.warning("Please enter some text before submitting.")
    else:
        if not OPENAI_API_KEY:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Display the markdown input
        st.subheader("Your Article:")
        st.markdown(markdown_input)
        
        # Add the markdown input to the messages
        st.session_state.messages.append({"role": "user", "content": markdown_input})
        st.chat_message("user").write(markdown_input)

        if "thread" not in st.session_state:
            st.session_state.thread = client.beta.threads.create()

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread.id,
            role="user",
            content=markdown_input
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=OPENAI_ASSISTANT_ID,
            model=OPENAI_MODEL
        )

        # Wait for the run to complete
        with st.spinner("AI Editor is reviewing your article..."):
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=run.id
                )

        # Retrieve the assistant's response
        messages = client.beta.threads.messages.list(thread_id=st.session_state.thread.id)
        assistant_message = next(msg for msg in messages if msg.role == "assistant")
        msg = assistant_message.content[0].text.value

        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)

# Display the conversation history
st.subheader("Conversation History:")
for msg in st.session_state.messages:
    st.text(f"{msg['role'].capitalize()}: {msg['content']}")