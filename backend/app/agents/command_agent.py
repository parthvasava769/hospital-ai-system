import re
from datetime import datetime, timedelta


class CommandAgent:

    @staticmethod
    def parse_command(command: str):

        command = command.lower()

        if "appointment" in command:
            return "book_appointment"

        if "bill" in command:
            return "view_bill"

        if "test" in command:
            return "create_lab_test"

        return "unknown"