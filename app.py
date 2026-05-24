import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"], 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.title("Campus Copilot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask about the campus..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        msg = response.choices[0].message.content
        st.chat_message("assistant").markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
    except Exception as e:
        st.error(f"Error: {e}")
