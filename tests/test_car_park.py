from pathlib import Path
import json
import unittest
from car_park import CarPark


class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.log_path = Path("test_log.txt")
        self.car_park = CarPark("123 Example Street", 100, log_file=self.log_path)



    def test_car_park_initialized_with_all_attributes(self):
            self.assertIsInstance(self.car_park, CarPark)
            self.assertEqual(self.car_park.location, "123 Example Street")
            self.assertEqual(self.car_park.capacity, 100)
            self.assertEqual(self.car_park.plates, [])
            self.assertEqual(self.car_park.displays, [])
            self.assertEqual(self.car_park.available_bays, 100)

    def test_add_car(self):
            self.car_park.add_car("FAKE-001")
            self.assertEqual(self.car_park.plates, ["FAKE-001"])
            self.assertEqual(self.car_park.available_bays, 99)

    def test_remove_car(self):
            self.car_park.add_car("FAKE-001")
            self.car_park.remove_car("FAKE-001")
            self.assertEqual(self.car_park.plates, [])
            self.assertEqual(self.car_park.available_bays, 100)

    def test_overfill_the_car_park(self):
            for i in range(100):
                self.car_park.add_car(f"FAKE-{i}")

            with self.assertRaises(ValueError):
                 self.car_park.add_car("FAKE-100")
            # Overfilling the car park should not change the number of available bays
            self.assertEqual(self.car_park.available_bays, 0)

            # Removing a car from an overfilled car park should not change the number of available bays
            with self.assertRaises(ValueError):
                self.car_park.remove_car("FAKE-100")
            self.assertEqual(self.car_park.available_bays, 0)

    def test_removing_a_car_that_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.car_park.remove_car("NO-1")

    def test_register_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.car_park.register("Not a Sensor or Display")

    def tearDown(self):
        if hasattr(self, "log_path"):
            self.log_path.unlink(missing_ok=True)

        Path("config.json").unlink(missing_ok=True)

    def test_write_config(self):
        self.car_park.write_config()

        config_path = Path("config.json")
        self.assertTrue(config_path.exists())
        with config_path.open() as f:
            data = json.load(f)

        self.assertEqual(data["location"], "123 Example Street")
        self.assertEqual(data["capacity"], 100)
        self.assertEqual(data["log_file"], str(self.log_path))

    def test_config_creates_car_park(self):
        self.car_park.write_config()

        new_car_park = CarPark.from_config()
        self.assertEqual(new_car_park.location, self.car_park.location)
        self.assertEqual(new_car_park.capacity, self.car_park.capacity)
        self.assertEqual(str(new_car_park.log_file), str(self.car_park.log_file))


if __name__ == "__main__":
    unittest.main()