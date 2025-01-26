from charging.domain.entities.charging_station import ChargingStation

class ChargingStationRepository:
    def get_all_stations(self):
        # Sample data
        data = [
            {"id": 1, "name": "Station A", "location": (52.5200, 13.4050), "postal_code": "10115", "status": "available"},
            {"id": 2, "name": "Station B", "location": (52.5300, 13.4100), "postal_code": "10115", "status": "occupied"},
        ]
        # Creating ChargingStation objects
        return [ChargingStation(**d) for d in data]
