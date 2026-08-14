
import json
import requests


class BookingAPIClient:

    def __init__(self, session) -> None:
        self.session = session

    def create_booking(self, payload):
        return self.session.post("/booking", json=payload)

# /booking/1
    def get_booking(self, booking_id):
        return self.session.get(f"/booking/{booking_id}")
