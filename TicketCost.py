from enum import Enum
from TicketType import TicketType


class TicketCost(Enum):
    FIRST_CLASS = 1000
    BUSINESS = 500
    ECONOMY = 250

    @staticmethod
    def get_ticket_cost(ticket_type: TicketType) -> float:
        return TicketCost[ticket_type.name].value


if __name__ == "__main__":
    print(f"First class ticket price: {TicketCost.get_ticket_cost(TicketType.FIRST_CLASS)}")
    print(f"Business class ticket price: {TicketCost.get_ticket_cost(TicketType.BUSINESS)}")
    print(f"Economy class ticket price: {TicketCost.get_ticket_cost(TicketType.ECONOMY)}")
