import streamlit as st
from api import register_user


def register_page():

    st.header("Register User")

    name = st.text_input("Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    password = st.text_input("Password", type="password")

    role = st.selectbox(
        "Role",
        ["patient", "doctor", "lab_staff"]
    )

    if st.button("Register"):

        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": password,
            "role": role
        }

        res = register_user(data)

        if res.status_code == 200:
            st.success("Registration successful")
        else:
            st.error(res.text)