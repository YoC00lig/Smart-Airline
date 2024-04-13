from datetime import datetime
from Airplane import Airplane

class Flight:
    """A class representing a flight.

    Attributes:
        flight_id (str): The unique identifier of the flight.
        airplane (Airplane): The airplane for this flight.
        destination (str): The destination airport of the flight.
        departure_time (datetime): The departure time of the flight.
        return_time (datetime): The return time of the airplane.
        capacity (int): The number of passengers already booked on this flight.
        cost (float): The cost of the flight.
    """
    def __init__(self, flight_id : str, airplane : Airplane, destination : str, departure_time : datetime, return_time : datetime, cost : float):
        self.flight_id = flight_id
        self.airplane = airplane
        self.destination = destination
        self.departure_time = departure_time
        self.return_time = return_time
        self.capacity = 0  
        self.cost = cost

    def add_passengers(self, number_of_passengers : int) -> bool:
        """Add passengers to the flight.

        Args:
            number_of_passengers (int): The number of passengers to add to the flight.
        
        Returns:
            bool: True if passengers were successfully added, False otherwise.
        """
        if self.capacity + number_of_passengers <= self.airplane.capacity:
            self.capacity += number_of_passengers
            return True
        else:
            return False

    def __str__(self):
        return f"Flight ID: {self.flight_id}\nAirplane ID: {self.airplane.airplane_id}\nDestination: {self.destination}\nDeparture Time: {self.departure_time}\nReturn Time: {self.return_time}\nCapacity: {self.capacity}\nCost: {self.cost}\n"
