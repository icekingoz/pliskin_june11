
import pytest
import requests

from api.booking_client import BookingAPIClient
from api.builders import make_booking

BASE_URL = "https://restful-booker.herokuapp.com"

class ApiSession(requests.Session):
    def request(self, method, url, **kwargs):
        kwargs.setdefault("timeout", 10)
        return super().request(method, BASE_URL + url, **kwargs)

@pytest.fixture(scope="session")
def api_session():
    session =  ApiSession()
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()

@pytest.fixture(scope="session")
def auth_token(api_session) -> str:
    r = requests.post(
        f"{BASE_URL}/auth",
        json={
            "username": "admin",
            "password": "password123"
        }
    )
    return r.json()["token"]


@pytest.fixture
def booking_client(api_session, auth_token):
    return BookingAPIClient(api_session, auth_token) 


@pytest.fixture
def created_booking(booking_client):
    payload = make_booking()
    booking_id = booking_client.create_booking(payload).json()["bookingid"]
    yield booking_id, payload
    
    booking_client.delete_booking(booking_id)   # the debt, paid — never asserted
