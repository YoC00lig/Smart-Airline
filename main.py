from Airport import Airport
from Airplane import Airplane
from Flight import Flight
from PassengerGroup import PassengerGroup, TicketType
from datetime import datetime
from messages import Messages

# TODO Change functiom from Airplane (i changed capacity to seats based on ticket type)

data_dict = {
    "airplanes": [
        {
            "id": "A1",
            "capacity": 200,
            "ticket_type": TicketType.BUSINESS
        },
        {
            "id": "A2",
            "capacity": 300,
            "ticket_type": TicketType.ECONOMY
        },
        {
            "id": "A3",
            "capacity": 250,
            "ticket_type": TicketType.BUSINESS
        }
    ],
    "passenger_groups": [
        {
            "id": "G1", "size": 150, "ticket_type": TicketType.BUSINESS, "destination": "Airport2",
            "flight_date": datetime(2024, 4, 20)
        },
        {
            "id": "G2", "size": 250, "ticket_type": TicketType.ECONOMY, "destination": "Airport3",
            "flight_date": datetime(2024, 4, 22)
        },
        {
            "id": "G3", "size": 100, "ticket_type": TicketType.BUSINESS, "destination": "Airport2",
            "flight_date": datetime(2024, 4, 21)
        },
        {
            "id": "G4", "size": 180, "ticket_type": TicketType.ECONOMY, "destination": "Airport4",
            "flight_date": datetime(2024, 4, 23)
        }
    ],
    "flights": [
        {
            "id": "F1",
            "airplane_id": "A1",
            "destination": "Airport2",
            "departure_date": datetime(2024, 4, 20),
            "return_date": datetime(2024, 4, 21),
            "cost": 1000.0
        },
        {
            "id": "F2",
            "airplane_id": "A2",
            "destination": "Airport3",
            "departure_date": datetime(2024, 4, 22),
            "return_date": datetime(2024, 4, 23),
            "cost": 1500.0
        }
    ]
}


def add_airplanes(airport):
    airplanes_data = data_dict["airplanes"]
    for data in airplanes_data:
        airplane = Airplane(data["id"], data["capacity"], data["ticket_type"])
        airport.add_airplane(airplane)


def add_passenger_groups(airport):
    passenger_groups_data = data_dict["passenger_groups"]
    for data in passenger_groups_data:
        passenger_group = PassengerGroup(data["id"], data["size"], data["ticket_type"], data["destination"], data["flight_date"])
        
        suitable_airplanes = airport.find_airplanes_for_passenger_group(passenger_group)
        if suitable_airplanes:
            chosen_airplane = suitable_airplanes[0]
            if passenger_group.size <= chosen_airplane.capacity:
                airport.add_passenger_group(passenger_group)
            else:
                raise Exception(Messages.PASSENGER_GROUP_CAPACITY_EXCEEDED.format(group_id=passenger_group.group_id))
        else:
            raise Exception(Messages.NO_SUITABLE_AIRPLANE.format(group_id=passenger_group.group_id))


def add_flights(airport):
    flights_data = data_dict["flights"]
    for data in flights_data:
        airplane = next((a for a in airport.airplanes if a.airplane_id == data["airplane_id"]), None)
        if airplane:
            if data["departure_date"] < data["return_date"]:
                flight = Flight(data["id"], airplane, data["destination"], data["departure_date"], data["return_date"], data["cost"])
                airport.add_flight(flight)
            else:
                raise Exception(Messages.FLIGHT_RETURN_DATE_INVALID.format(flight_id=data['id']))


def create_airport():
    airport = Airport("Airport1")

    try:
        add_airplanes(airport)
        add_passenger_groups(airport)
        add_flights(airport)
    except Exception as e:
        raise Exception(f"Error when creating airport: {str(e)}")

    return airport


def main():
    try:
        airport = create_airport()
        print(airport)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
