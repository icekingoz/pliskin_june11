from uuid import uuid4


def make_booking(**overrides):
    booking = {
        "firstname": f"qa-{uuid4().hex[:8]}",   # ← unique EVERY call
        "lastname": "Snake",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-09-01",
            "checkout": "2026-09-05",
        },
        "additionalneeds": "Breakfast",
    }
    booking.update(overrides)
    return booking
