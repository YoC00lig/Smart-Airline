from enum import Enum
from Ticket import TicketType

class TicketCost(Enum):
    # INTERNATIONAL = 1000
    # DOMESTIC = 500
    FIRST_CLASS = 1000
    BUSINESS = 500
    ECONOMY = 250

    # get_ticket_cost(ticket_type: TicketType) -> float: Get the cost of a ticket based on its type.
    @staticmethod
    def get_ticket_cost(ticket_type):
        return TicketCost[ticket_type.name].value
    
if __name__ == "__main__":
    print(TicketCost.get_ticket_cost(TicketType.FIRST_CLASS))
    print(TicketCost.get_ticket_cost(TicketType.BUSINESS))
    print(TicketCost.get_ticket_cost(TicketType.ECONOMY))