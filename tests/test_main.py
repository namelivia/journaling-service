from mock import patch, Mock
from freezegun import freeze_time
import datetime
from .test_base import (
    client,
    create_test_database,
    database_test_session,
)
import uuid
from app.models import Entry
from app.schemas import Entry as EntrySchema


@freeze_time("2013-04-09")
class TestApp:
    def _insert_test_entry(self, session, entry: dict = {}):
        data = {
            "message": "Test message",
            "timestamp": datetime.datetime.now(),
        }
        data.update(entry)
        db_entry = Entry(**data)
        session.add(db_entry)
        session.commit()
        return db_entry

    def test_create_entry(self, client):
        key = uuid.uuid4()
        response = client.post(
            "/new",
            json={
                "message": "Test message",
                "key": str(key),
            },
        )
        assert response.status_code == 201
        assert response.json() == {
            "id": 1,
            "message": "Test message",
            "key": str(key),
            "timestamp": "2013-04-09T00:00:00",
        }

    def test_create_entry_invalid(self, client):
        response = client.post("/new", json={"message": None})
        assert response.status_code == 422

    def test_get_all_entries(self, client, database_test_session):
        key = uuid.uuid4()
        self._insert_test_entry(database_test_session, {"key": key})
        self._insert_test_entry(database_test_session, {"key": key})
        response = client.get(f"/{str(key)}/all")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "message": "Test message",
                "timestamp": "2013-04-09T00:00:00",
                "key": str(key),
            },
            {
                "id": 2,
                "message": "Test message",
                "timestamp": "2013-04-09T00:00:00",
                "key": str(key),
            },
        ]
        response = client.get(f"/{str(uuid.uuid4())}/all")
        assert response.status_code == 200
        assert response.json() == []
