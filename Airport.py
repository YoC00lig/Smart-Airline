from Flight import Flight
from Airplane import Airplane
from PassengerGroup import PassengerGroup

class Airport:
    """A class representing our main airport.

    Attributes:
        airport_id (str): The unique identifier of the airport.
        airplanes (list): A list containing information about available airplanes at the airport.
        flights (list): A list containing information about scheduled flights from the airport.
        passenger_groups (list): A list containing information about passenger groups at the airport.
    """
    def __init__(self, airport_id : str):
        self.airport_id = airport_id
        self.airplanes = []
        self.flights = []
        self.passenger_groups = []

    def add_flight(self, flight : Flight):
        """Add a flight to the list of scheduled flights."""
        self.flights.append(flight)

    def add_airplane(self, airplane : Airplane):
        """Add an airplane to the list of available airplanes."""
        self.airplanes.append(airplane)
    
    def add_passenger_group(self, passenger_group : PassengerGroup):
        """Add a passenger group to the list of groups."""
        self.passenger_groups.append(passenger_group)
    
    def find_airplanes_for_passenger_group(self, passenger_group : PassengerGroup) -> list:
        """Find appropriate airplanes for the given passenger group.

        Args:
            passenger_group (PassengerGroup): The passenger group for which to find airplanes.

        Returns:
            list: A list of appropriate airplanes for the passenger group.
        """
        matching_airplanes = []
        for airplane in self.airplanes:
            if airplane.capacity >= passenger_group.size and airplane.ticket_type == passenger_group.ticket_type:
                matching_airplanes.append(airplane)
        return matching_airplanes
    
    def schedule_flight_for_passenger_group(self, passenger_group : PassengerGroup) -> Flight:
        """Schedule a flight for the given passenger group.

        Args:
            passenger_group (PassengerGroup): The passenger group for which to schedule the flight.

        Returns:
            Flight or None: The scheduled flight for the passenger group, or None if no suitable airplane is found.
        """
        matching_airplanes = self.find_airplanes_for_passenger_group(passenger_group)

        if matching_airplanes:
            for flight in self.flights:
                if (flight.destination == passenger_group.destination and 
                    flight.airplane_id in [airplane.airplane_id for airplane in matching_airplanes] and
                    flight.departure_time.date() == passenger_group.flight_date.date()):  
                    if flight.capacity + passenger_group.size <= flight.airplane.capacity:
                        flight.capacity += passenger_group.size
                        return flight

            flight_id = f"Flight_{len(self.flights) + 1}"
            cost = 0 #### TODO
            flight = Flight(flight_id, matching_airplanes[0], passenger_group.destination, passenger_group.flight_date, passenger_group.flight_date, cost)
            self.flights.append(flight)
            return flight
        else:
            return None


