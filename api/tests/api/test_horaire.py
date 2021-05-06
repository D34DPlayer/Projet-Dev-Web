from api.schemas import Horaire, DayHoraire
from fastapi import status
from fastapi.testclient import TestClient


class TestHoraire:
    schedule = Horaire(
        lu=DayHoraire(),
        ma=DayHoraire(is_open=True, open="08:00:00", close="18:00:00"),
        me=DayHoraire(is_open=True, open="08:00:00", close="18:00:00"),
        je=DayHoraire(is_open=True, open="08:00:00", close="18:00:00"),
        ve=DayHoraire(is_open=True, open="08:00:00", close="18:00:00"),
        sa=DayHoraire(is_open=True, open="08:00:00", close="18:00:00"),
        di=DayHoraire()
    )

    def test_update_horaire(self, client: TestClient, headers: dict):
        # Check for authorizations
        response = client.put("/horaire", json=self.schedule.dict())
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # Update the schedule
        response = client.put("/horaire", json=self.schedule.dict(), headers=headers)
        assert response.status_code == status.HTTP_200_OK

    def test_get_horaire(self, client: TestClient):
        # Check the updated schedule
        response = client.get("/horaire")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == self.schedule
