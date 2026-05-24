import streamlit as st
from openai import OpenAI

# Replace the text below with your actual API Key
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"], 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.title("Campus Copilot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about the campus..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="gemini-1.5-flash",
        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    )
    
    msg = response.choices[0].message.content
    with st.chat_message("assistant"):
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
