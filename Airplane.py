from Ticket import TicketType

class Airplane:
    """A class representing an airplane.

    Attributes:
        airplane_id (str): The unique identifier of the airplane.
        capacity (int): The maximum number of passengers.
        ticket_type (TicketType): Available ticket type (international or domestic).
    """

    def __init__(self, airplane_id : str, capacity : int, ticket_type : TicketType):
        self.airplane_id = airplane_id
        self.capacity = capacity
        self.ticket_type = ticket_type