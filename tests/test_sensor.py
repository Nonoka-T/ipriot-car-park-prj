import unittest
from sensor import EntrySensor
from sensor import ExitSensor
from car_park import CarPark

class TestSensor(unittest.TestCase):
    def setUp(self):
        self.car_park = CarPark("Test", 100)
        self.entry_sensor = EntrySensor(1, True, self.car_park)
        self.exit_sensor = ExitSensor(2, True, self.car_park)

    def test_entry_sensor(self):
        self.assertEqual(self.entry_sensor.id, 1)
        self.assertTrue(self.entry_sensor.car_park, self.car_park)
        self.assertIs(self.entry_sensor.car_park, self.car_park)

    def test_exit_sensor(self):
        self.assertEqual(self.exit_sensor.id, 2)
        self.assertTrue(self.exit_sensor.is_active)
        self.assertIs(self.exit_sensor.car_park, self.car_park)

    def test_entry_sensor_detect(self):
        initial_count = len(self.car_park.plates)
        self.entry_sensor.detect_vehicle()
        self.assertEqual(len(self.car_park.plates), initial_count + 1)

    def test_exit_sensor_detect(self):
        self.car_park.add_car("FAKE-001")
        initial_count = len(self.car_park.plates)
        self.exit_sensor.detect_vehicle()
        self.assertEqual(len(self.car_park.plates), initial_count - 1)