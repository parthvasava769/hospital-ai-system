import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

def ai_agent_page():

    st.header("Hospital AI Assistant")

    user_input = st.text_input("Enter your request")

    if st.button("Submit"):

        res = requests.post(
            f"{BASE_URL}/ai-assistance/command",
            json={"command": user_input},
            params={"user_id": st.session_state["user_id"]}
        )

        if res.status_code == 200:
            st.write(res.json())
        else:
            st.error(res.text)