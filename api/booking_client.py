class BookingAPIClient:

    def __init__(self, session, token=None) -> None:
        self.session = session
        self.token = token

    def _auth_headers(self):
        return {"Cookie": f"token={self.token}"}

    def create_booking(self, payload):
        return self.session.post("/booking", json=payload)

# /booking/1
    def get_booking(self, booking_id):
        return self.session.get(f"/booking/{booking_id}")

    def get_booking_ids(self, **filters):
        return self.session.get("/booking", params=filters)

    def update_booking(self, booking_id, payload):
        return self.session.put(
            f"/booking/{booking_id}",
            json=payload,
            headers=self._auth_headers(),
        )
    
    def patch_booking(self, booking_id, changes):
        """PATCH — changes SOME fields. (Added during classwork.)"""
        return self.session.patch(
            f"/booking/{booking_id}",
            json=changes,
            headers=self._auth_headers(),
        )

    # ------------------------------------------------------------- Delete
    def delete_booking(self, booking_id):
        """The LAST method — added in Lesson 17. The client is complete."""
        return self.session.delete(
            f"/booking/{booking_id}",
            headers=self._auth_headers(),
        )