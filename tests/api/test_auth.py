import requests
from urllib3.util import response

# Creates a new auth token to use for access to the PUT and DELETE /booking

# post
# https://restful-booker.herokuapp.com/auth

# Header
# Field	Type	Description
# Content-Type	string	
# Sets the format of payload you are sending

# Default value: application/json

# Request body
# Field	Type	Description
# username	String	
# Username for authentication

# Default value: admin

# password	String	
# Password for authentication

# Success 200
# Field	Type	Description
# token	String	
# Token to use in future requests

# Response:
# HTTP/1.1 200 OK

# {
#     "token": "abc123"
# }

# {
#     "username": "asdsds"

# }

BASE_URL = "https://restful-booker.herokuapp.com"

def test_get_token():
    # Create and send the request (use the appropirate method)
    response = requests.post(
        f"{BASE_URL}/auth",
        json={
            "username": "admin",
            "password": "password123"
        },
        timeout=10,
    )
    # Check actual data and code
    assert response.status_code == 200
    assert response.json()["token"]

    # {
    #   key        value
    # "token": "eda6750a5d6d8a7"
    # }

def test_ping():
    response = requests.get(
         f"{BASE_URL}/ping",
         timeout=10
    )
    assert response.status_code == 201
    # 201 is a bug. 200 is what is expected.
