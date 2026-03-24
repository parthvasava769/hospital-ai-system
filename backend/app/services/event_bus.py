class EventBus:
    """
    Simple event bus for publishing and subscribing to events.
    Agents can register handlers for specific events.
    """

    _subscribers = {}

    @classmethod
    def subscribe(cls, event_name: str, handler):
        if event_name not in cls._subscribers:
            cls._subscribers[event_name] = []

        cls._subscribers[event_name].append(handler)

    @classmethod
    def publish(cls, event_name: str, data):

        handlers = cls._subscribers.get(event_name, [])

        for handler in handlers:
            handler(data)


