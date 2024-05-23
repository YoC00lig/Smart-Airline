# class for generation pseudo random data
import random
from datetime import datetime, timedelta
from PassengerGroup import TicketType

# example:
# data_dict = {
#     "airplanes": [
#         {"id": "A1", "capacity": 200, "ticket_type": TicketType.DOMESTIC},
#         {"id": "A2", "capacity": 300, "ticket_type": TicketType.INTERNATIONAL},
#         {"id": "A3", "capacity": 250, "ticket_type": TicketType.DOMESTIC}
#     ],
#     "passenger_groups": [
#         {"id": "G1", "size": 150, "ticket_type": TicketType.DOMESTIC, "destination": "Airport2", "flight_date": datetime(2024, 4, 20)},
#         {"id": "G2", "size": 250, "ticket_type": TicketType.INTERNATIONAL, "destination": "Airport3", "flight_date": datetime(2024, 4, 22)},
#         {"id": "G3", "size": 100, "ticket_type": TicketType.DOMESTIC, "destination": "Airport2", "flight_date": datetime(2024, 4, 21)},
#         {"id": "G4", "size": 180, "ticket_type": TicketType.INTERNATIONAL, "destination": "Airport4", "flight_date": datetime(2024, 4, 23)}
#     ],
#     "flights": [
#         {"id": "F1", "airplane_id": "A1", "destination": "Airport2", "departure_date": datetime(2024, 4, 20), "return_date": datetime(2024, 4, 21), "cost": 1000.0},
#         {"id": "F2", "airplane_id": "A2", "destination": "Airport3", "departure_date": datetime(2024, 4, 22), "return_date": datetime(2024, 4, 23), "cost": 1500.0}
#     ]
# }


class Generator:
    """A class for generating pseudo random data for testing purposes.

    Attributes:

    Methods:
        generate_airplanes(n : int) -> list: Generate a list of n airplanes with random capacities.
        generate_passenger_groups(n : int, n_airports : int) -> list: Generate a list of n passenger groups with random sizes, ticket types, destinations and flight dates.
        generate_random_test_data(n_airplanes : int, n_passenger_groups : int, n_airports : int) -> dict: Generate a dictionary with random airplanes, passenger groups and empty flights.
        generate_many_random_test_data(n : int) -> list: Generate a list of n random data dictionaries.
        print_data_dict(data_dict: dict): Print the data dictionary.

    """

    @staticmethod
    def generate_airplanes(n: int):
        airplanes = {}
        for i in range(1, n + 1):
            airplane_id = f"A{i}"
            seats = {}
            for ticket_type in TicketType:
                match ticket_type:
                    case TicketType.FIRST_CLASS:
                        capacity = random.randrange(20, 50, 10)
                    case TicketType.BUSINESS:
                        capacity = random.randrange(50, 100, 10)
                    case TicketType.ECONOMY:
                        capacity = random.randrange(100, 200, 10)
                    case _:
                        capacity = 100
                seats[ticket_type] = capacity

            airplanes[airplane_id] = seats
        return airplanes

    @staticmethod
    def generate_passenger_groups(n: int, n_airports: int):
        passenger_groups = {}
        airports = [f"Airport{i}" for i in range(2, n_airports + 2)]
        for i in range(1, n + 1):
            group_id = f"G{i}"
            size = random.randint(10, 40)
            ticket_type = random.choice(list(TicketType))
            destination = random.choice(airports)
            flight_date = (datetime.now() + timedelta(days=random.randint(1, 5))).date()
            passenger_groups[group_id] = \
                {"size": size, "ticket_type": ticket_type, "destination": destination, "flight_date": flight_date}
        return passenger_groups, airports

    @staticmethod
    def generate_random_test_data(number_of_airplanes: int, number_of_passenger_groups: int, number_of_airports: int):
        airplanes = Generator.generate_airplanes(number_of_airplanes)
        passenger_groups, airports = Generator.generate_passenger_groups(number_of_passenger_groups, number_of_airports)
        airports = {airport: random.choice([1400, 2000]) for airport in airports}

        return {
            "airplanes": airplanes,
            "passenger_groups": passenger_groups,
            "airports": airports
        }
    
    @staticmethod
    def generate_many_random_test_data(n: int):
        data_dicts = []
        for _ in range(n):
            number_of_airplanes = random.randint(2, 10)
            number_of_passenger_groups = random.randint(5, 10)
            number_of_airports = random.randint(2, 10)
            data_dicts.append(
                Generator.generate_random_test_data(
                    number_of_airplanes,
                    number_of_passenger_groups,
                    number_of_airports
                )
            )
        return data_dicts
    
    @staticmethod 
    def print_test_data(test_data: dict):
        print("Airplanes:")
        for idx, airplane in test_data["airplanes"].items():
            print(f"{idx}: {airplane}")
        print("\nPassenger Groups:")
        for idx, passenger_group in test_data["passenger_groups"].items():
            print(f"{idx}: {passenger_group}")
        print("\nFlights:")
        for flight in test_data["flights"]:
            print(flight)


if __name__ == "__main__":
    # Example usage
    random_test_data = Generator.generate_random_test_data(3, 4, 3)
    Generator.print_test_data(random_test_data)
