from openai import OpenAI
import streamlit as st

from constants import OPENAI_API_KEY, OPENAI_ASSISTANT_ID, OPENAI_MODEL

st.title("✍️ AI Editor")
st.caption("🇺🇦 Article editor powered by UActuality")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "I'm your AI Editor. Show me your article?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not OPENAI_API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=OPENAI_API_KEY)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if "thread" not in st.session_state:
        st.session_state.thread = client.beta.threads.create()

    client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=OPENAI_ASSISTANT_ID,
        model=OPENAI_MODEL
    )

    # Wait for the run to complete
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