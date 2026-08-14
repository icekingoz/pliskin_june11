import re
import requests

from api.booking_client import BookingAPIClient
from api.builders import make_booking


# Request
# curl -X POST \
#   https://restful-booker.herokuapp.com/booking \
#   -H 'Content-Type: application/json' \
#   -d '{
#     "firstname" : "Jim",
#     "lastname" : "Brown",
#     "totalprice" : 111,
#     "depositpaid" : true,
#     "bookingdates" : {
#         "checkin" : "2018-01-01",
#         "checkout" : "2019-01-01"
#     },
#     "additionalneeds" : "Breakfast"
# }'

def test_create_booking(booking_client: BookingAPIClient):
    payload= make_booking()
    response = booking_client.create_booking(payload)

    assert response.status_code == 200
    assert response.json()["bookingid"] 
    assert response.json()["booking"] == payload

# json={
#     "key": "value",
#     "nest": {
#         "key1":"value1", 
#         "key2":"value2" 
#         }
#     }
# json["key"]
# json.keys[0]
# json.values[0]
# json["nest"]["key1"]

def test_create_without_field(booking_client: BookingAPIClient):
    payload = make_booking()
    del payload["bookingdates"]
    r = booking_client.create_booking(payload)
    print(r.status_code) # 400
    assert r.status_code == 500



# Response
# HTTP/1.1 200 OK

# {
#     "bookingid": 1,
#     "booking": {
#         "firstname": "Jim",
#         "lastname": "Brown",
#         "totalprice": 111,
#         "depositpaid": true,
#         "bookingdates": {
#             "checkin": "2018-01-01",
#             "checkout": "2019-01-01"
#         },
#         "additionalneeds": "Breakfast"
#     }
# }