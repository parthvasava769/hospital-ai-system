from app.models.billing import Billing


class BillingAgent:

    @staticmethod
    def generate_invoice(db, appointment):

        bill = Billing(
            patient_id=appointment.patient_id,
            appointment_id=appointment.id,
            amount=500.0,   # fixed consultation fee
            status="Pending"
        )

        db.add(bill)
        db.commit()
        db.refresh(bill)

        return bill