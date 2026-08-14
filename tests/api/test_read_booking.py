
# ------------------------------------------------ Test 1 — the roundtrip
from api.booking_client import BookingAPIClient


def test_created_booking_reads_back(booking_client: BookingAPIClient, created_booking):
    booking_id, payload = created_booking     # fresh data, made for THIS test

    r = booking_client.get_booking(booking_id)

    assert r.status_code == 200
    assert r.json() == payload    # GET returns NO wrapper — whole echo, one ==


# ------------------------------------------------ Stretch — negative Read
def test_missing_booking_is_404(booking_client):
    r = booking_client.get_booking(999999)
    assert r.status_code == 404   # same friend as Lesson 14 — now via the client
