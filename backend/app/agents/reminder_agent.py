import smtplib
from email.mime.text import MIMEText

class ReminderAgent:

    @staticmethod
    def send_reminder(appointment):

        print("Reminder function triggered")

        try:
            sender_email = "parthvasava62352@gmail.com"
            sender_password = "tejqcxbkuecsfuti"


            # ✅ SAFE EMAIL EXTRACTION
            receiver_email = None

            if appointment.patient and appointment.patient.email:
                receiver_email = appointment.patient.email

            if not receiver_email:
                print("❌ No email found for patient")
                return

            print("Sending to:", receiver_email)

            subject = "Appointment Update"

            body = f"""
Hello,

Your appointment has been updated.

Status: {appointment.status}
Date: {appointment.appointment_date}

Thank you.
"""

            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = sender_email
            msg["To"] = receiver_email

            print("Connecting to SMTP...")

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)

            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()

            print("✅ Email sent successfully")

        except Exception as e:
            print("❌ Email Error:", e)