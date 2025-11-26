from sensor import Sensor
from display import Display

class CarPark:
    def __init__(self, location, capacity, plates = None, displays = None, sensors = None):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.displays = displays or []
        self.sensors = sensors or []

    def __str__(self):
        return f"Car park at {self.location} with capacity {self.capacity} bays."

    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")

        elif isinstance(component, Display):
            self.displays.append(component)

    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()

    def remove_car(self, plate):
        if plate in self.plates:
            self.plates.remove(plate)
            self.update_displays()

    def update_displays(self):
        for display in self.displays:
            display.update()

    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))