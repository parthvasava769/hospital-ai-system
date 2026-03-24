import requests

BASE_URL = "http://127.0.0.1:8000"


def register_user(data):
    return requests.post(f"{BASE_URL}/auth/register", params=data)


def login_user(data):
    return requests.post(f"{BASE_URL}/auth/login", params=data)


def create_appointment(data, user_id):

    return requests.post(
        f"{BASE_URL}/appointments",
        json=data,
        params={"user_id": user_id}
    )


def get_appointments():
    return requests.get(f"{BASE_URL}/appointments")


def create_lab_test(data):
    return requests.post(f"{BASE_URL}/lab-tests", params=data)

def get_doctors():
    return requests.get(f"{BASE_URL}/users?role=doctor")


def ai_assist(symptoms):
    return requests.post(
        f"{BASE_URL}/ai-assistance/analyze",
        json={"symptoms": symptoms}
    )

def get_lab_tests():
    return requests.get(f"{BASE_URL}/lab-tests")

def update_appointment_status(appointment_id, status):
    return requests.put(
        f"http://127.0.0.1:8000/appointments/{appointment_id}/status",
        json={"status": status}
    )

def get_my_appointments(user_id):
    return requests.get(f"{BASE_URL}/appointments/patient/{user_id}")