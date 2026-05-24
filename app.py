import streamlit as st
from openai import OpenAI

# 1. Initialize the client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"], 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

st.title("Campus Copilot")

# 2. Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Handle user input
if prompt := st.chat_input("Ask about the campus..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # 5. Get response with clean message formatting
        response = client.chat.completions.create(
            model="gemini-1.5-flash",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        
        msg = response.choices[0].message.content
        st.chat_message("assistant").markdown(msg)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        # If it fails, clear history so the next attempt starts fresh
        st.session_state.messages = []
