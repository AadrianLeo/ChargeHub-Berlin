import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


from charging.domain.entities.charging_station import ChargingStation
from charging.infrastructure.repositories.charging_station_repository import ChargingStationRepository

class TestChargingStationRepository(unittest.TestCase):

    def setUp(self):
        # Initialize the repository before each test
        self.repository = ChargingStationRepository()

    def test_get_all_stations(self):
        # Call the method to get all charging stations
        stations = self.repository.get_all_stations()

        # Debugging: Print the types of the items
        for station in stations:
            print(f"Type of station: {type(station)}")

        # Assert that the result is a list of ChargingStation objects
        self.assertIsInstance(stations, list)
        self.assertTrue(all(isinstance(station, ChargingStation) for station in stations))


        # Test the first station
        first_station = stations[0]
        self.assertEqual(first_station.id, 1)
        self.assertEqual(first_station.name, "Station A")
        self.assertEqual(first_station.location, (52.5200, 13.4050))
        self.assertEqual(first_station.postal_code, "10115")
        self.assertEqual(first_station.status, "available")

        # Test the second station
        second_station = stations[1]
        self.assertEqual(second_station.id, 2)
        self.assertEqual(second_station.name, "Station B")
        self.assertEqual(second_station.location, (52.5300, 13.4100))
        self.assertEqual(second_station.postal_code, "10115")
        self.assertEqual(second_station.status, "occupied")

if __name__ == "__main__":
    unittest.main()
