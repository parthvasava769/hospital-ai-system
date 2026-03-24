import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

def ai_dashboard():

    st.header("AI Symptom Assistant")

    symptoms = st.text_input("Enter symptoms")

    if st.button("Analyze Symptoms"):

        with st.spinner("🤖 AI is analyzing symptoms..."):

            res = requests.post(
                f"{BASE_URL}/ai-assistance/analyze",
                json={"symptoms": symptoms}
            )

            if res.status_code == 200:

                data = res.json()

                conditions = "".join([f"<li>{c}</li>" for c in data["possible_conditions"]])
                tests = "".join([f"<li>{t}</li>" for t in data["recommended_tests"]])

                st.markdown(f"""
                    <div style="
                        background-color:#1e1e1e;
                        padding:20px;
                        border-radius:12px;
                        border-left:6px solid #00c6ff;
                        margin-top:15px;
                    ">
                        <h3 style="color:#00c6ff;">🤖 AI Health Analysis</h3>
                        <hr style="border:1px solid #333;">
                        <h4>Possible Conditions</h4>
                        <ul>{conditions}</ul>
                        <h4>Recommended Tests</h4>
                        <ul>{tests}</ul>

                    </div>
                    """, 
                    unsafe_allow_html=True
                )

            else:
                st.error(res.text)