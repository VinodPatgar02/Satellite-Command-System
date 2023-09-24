import logging

# Define custom exceptions for specific error cases.
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

# Create a decorator for handling transient errors gracefully.
def transient_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TransientError as e:
            logging.warning(f"Transient Error: {e}")  # Log transient errors.
            print(f"Transient Error: {e}")  # Print transient errors.
    return wrapper

# Define the Satellite class to represent the satellite and its behavior.
class Satellite:
    def __init__(self):
        # Initialize the satellite's initial state.
        self.orientation = "North"
        self.solar_panels = "Inactive"
        self.data_collected = 0

    # Method to rotate the satellite's orientation.
    def rotate(self, direction):
        valid_directions = ["North", "South", "East", "West"]
        if direction in valid_directions:
            self.orientation = direction
            logging.info(f"Rotated to {direction}.")  # Log the rotation.
        else:
            raise InvalidDirectionError("Invalid direction. Use 'North', 'South', 'East', or 'West'.")

    # Method to set the solar panel status.
    def set_solar_panels(self, status):
        if self.solar_panels == status:
            raise TransientError(f'Solar panels are already {status.lower()}.')
        self.solar_panels = status
        logging.info(f'Solar panels {status.lower()}ed.')  # Log the change in solar panel status.

    # Methods with transient error handling decorators to activate, deactivate, and collect data.
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
            logging.info("Data collected.")  # Log data collection.
        else:
            raise InactiveSolarPanelsError("Cannot collect data with inactive solar panels.")

# The main function where the program execution begins.
def main():
    # Configure logging to log events to a file.
    logging.basicConfig(filename='satellite.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Create an instance of the Satellite class.
    satellite = Satellite()
    logging.info("Satellite initialized.")  # Log satellite initialization.
    
    # Display the initial state of the satellite.
    print("Initial State:")
    print(f"Orientation: {satellite.orientation}")
    print(f"Solar Panels: {satellite.solar_panels}")
    print(f"Data Collected: {satellite.data_collected}")
    print()

    while True:
        # Accept user commands to interact with the satellite.
        command = input("Enter a command (rotate, activatePanels, deactivatePanels, collectData, status, or exit): ")
        
        if command == "exit":
            break

        try:
            # Execute user commands and log relevant events.
            if command == "rotate":
                direction = input("Enter a direction (North, South, East, West): ")
                satellite.rotate(direction)
            elif command == "activatePanels":
                satellite.activate_panels()
            elif command == "deactivatePanels":
                satellite.deactivate_panels()
            elif command == "collectData":
                satellite.collect_data()
            elif command == "status":
                # Display the current status when requested.
                print("Current State:")
                print(f"Orientation: {satellite.orientation}")
                print(f"Solar Panels: {satellite.solar_panels}")
                print(f"Data Collected: {satellite.data_collected}")
            else:
                print("Invalid command. Please try again.")
                continue
        except (InvalidDirectionError, SolarPanelsAlreadyActiveError, SolarPanelsAlreadyInactiveError, InactiveSolarPanelsError) as e:
            print(f"Error: {e}")
            logging.error(f"Error: {e}")  # Log errors.

# Execute the main function if this script is run.
if __name__ == "__main__":
    main()
