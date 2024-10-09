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
        st.session_state.thread = client.assistant.threads.create(
            model=OPENAI_MODEL,
            messages=st.session_state.messages,
            assistant_id=OPENAI_ASSISTANT_ID,
        )
    else:
        st.session_state.thread.update(messages=st.session_state.messages)

    response = st.session_state.thread.run()
    msg = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)