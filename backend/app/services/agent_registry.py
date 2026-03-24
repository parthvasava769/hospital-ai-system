from app.services.event_bus import EventBus
from app.services.events import Events

from app.agents.notification_agent import NotificationAgent
from app.agents.billing_agent import BillingAgent


def register_agents():

    # Appointment created
    EventBus.subscribe(
        Events.APPOINTMENT_CREATED,
        NotificationAgent.send_appointment_confirmation
    )

    EventBus.subscribe(
        Events.APPOINTMENT_CREATED,
        BillingAgent.generate_invoice
    )

    # Appointment cancelled
    EventBus.subscribe(
        Events.APPOINTMENT_CANCELLED,
        NotificationAgent.send_appointment_cancellation
    )