"""Delete + the full roundtrip — built TOGETHER in class (slides 5–6).

Run just this file:  pytest tests/api/test_delete_booking.py -v
"""
from api.builders import make_booking


def test_deleted_booking_is_gone(booking_client, created_booking):
    booking_id, payload = created_booking

    r = booking_client.delete_booking(booking_id)
    assert r.status_code == 201      # BUG: 201 Created… for a DELETE. Logged.

    assert booking_client.get_booking(booking_id).status_code == 404
    # gone means UNFINDABLE, not "the server said OK".
    # (the fixture's teardown will delete this id again — and must not mind.)


def test_full_booking_lifecycle(booking_client):
    """Every verb of the block, one readable story. The interview classic."""
    payload = make_booking()
    booking_id = booking_client.create_booking(payload).json()["bookingid"]   # C
    assert booking_client.get_booking(booking_id).json() == payload           # R

    updated = make_booking(totalprice=999)
    booking_client.update_booking(booking_id, updated)                        # U
    assert booking_client.get_booking(booking_id).json() == updated

    booking_client.delete_booking(booking_id)                                 # D
    assert booking_client.get_booking(booking_id).status_code == 404          # proof
    # no fixture needed — the lifecycle is its own arrange, act and cleanup.
