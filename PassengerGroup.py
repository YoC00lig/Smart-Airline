from TicketType import TicketType
from datetime import datetime


class PassengerGroup:
    """A class representing a group of passengers.

    Attributes:
        group_id (str): The unique identifier of the passenger group.
        size (int): The number of passengers in the group.
        ticket_type (TicketType): The preferred ticket type for the group.
        destination (str): The destination airport of the group.
        flight_date (datetime): The planned date of the flight.
    """
    def __init__(self, group_id: str, size: int, ticket_type: TicketType, destination: str, flight_date: datetime):
        self.group_id = group_id
        self.size = size
        self.ticket_type = ticket_type
        self.destination = destination
        self.flight_date = flight_date

    def __str__(self):
        return (f"Group ID: {self.group_id}\n"
                f"Size: {self.size}\n"
                f"Ticket Type: {self.ticket_type.value}\n"
                f"Destination: {self.destination}\n"
                f"Flight Date: {self.flight_date}\n")
