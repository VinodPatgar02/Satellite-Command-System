import logging
from enum import Enum

class InvalidDirectionError(Exception):
    pass

class SolarPanelsAlreadyActiveError(Exception):
    pass

class SolarPanelsAlreadyInactiveError(Exception):
    pass

class InactiveSolarPanelsError(Exception):
    pass

class TransientError(Exception):
    pass

class Direction(Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

def transient_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TransientError as e:
            logging.exception(f"Transient Error: {e}")
            print(f"Transient Error: {e}")
    return wrapper

class Satellite:
    def __init__(self):
        self.orientation = Direction.NORTH
        self.solar_panels = "Inactive"
        self.data_collected = 0

    def rotate(self, direction):
        if direction not in Direction._value2member_map_:
            raise InvalidDirectionError("Invalid direction. Use 'North', 'South', 'East', or 'West'.")
        self.orientation = direction
        logging.info(f"Rotated to {direction}.")

    def set_solar_panels(self, status):
        if self.solar_panels == status:
            raise TransientError(f'Solar panels are already {status.lower()}.')
        self.solar_panels = status
        logging.info(f'Solar panels {status.lower()}ed.')

    @transient_error_handler
    def activate_panels(self):
        self.set_solar_panels("Active")

    @transient_error_handler
    def deactivate_panels(self):
        self.set_solar_panels("Inactive")

    @transient_error_handler
    def collect_data(self):
        if self.solar_panels == "Active":
            self.data_collected += 10
            logging.info("Data collected.")
        else:
            raise InactiveSolarPanelsError("Cannot collect data with inactive solar panels.")

def print_satellite_state(satellite):
    print("Current State:")
    print(f"Orientation: {satellite.orientation.value}")
    print(f"Solar Panels: {satellite.solar_panels}")
    print(f"Data Collected: {satellite.data_collected}")

def main():
    logging.basicConfig(filename='satellite.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    satellite = Satellite()
    logging.info("Satellite initialized.")
    
    print_satellite_state(satellite)

    while True:
        command = input("Enter a command (rotate, activatePanels, deactivatePanels, collectData, status, or exit): ")
        
        if command == "exit":
            break

        try:
            if command == "rotate":
                direction = input("Enter a direction (North, South, East, West): ")
                satellite.rotate(Direction[direction])
            elif command == "activatePanels":
                satellite.activate_panels()
            elif command == "deactivatePanels":
                satellite.deactivate_panels()
            elif command == "collectData":
                satellite.collect_data()
            elif command == "status":
                print_satellite_state(satellite)
            else:
                print("Invalid command. Please try again.")
                continue
        except (InvalidDirectionError, SolarPanelsAlreadyActiveError, SolarPanelsAlreadyInactiveError, InactiveSolarPanelsError) as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
