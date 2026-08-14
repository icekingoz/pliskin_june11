


def make_booking(**overrides):
    booking = {
        "firstname" : "Solid",
        "lastname" : "Snake",
        "totalprice" : 111,
        "depositpaid" : True,
        "bookingdates" : {
            "checkin" : "2018-09-01",
            "checkout" : "2019-09-05"
        },
        "additionalneeds" : "Breakfast"
    }
    booking.update(overrides)
    return booking

# make_booking()
# make_booking(
#     first="Liquid",
#     last_name="Geko"
# )