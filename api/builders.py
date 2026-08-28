from uuid import uuid4


def make_booking(**overrides):
    uuid = uuid4().hex[:8] # 3f7ff34x
    booking = {
        "firstname" : f"Solid{uuid}",
        "lastname" : f"Snake{uuid}",
        "totalprice" : 111,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-09-01",
            "checkout" : "2019-09-05"
        },
        "additionalneeds": "Breakfast",
    }
    booking.update(overrides)
    return booking
