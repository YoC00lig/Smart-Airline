import pytest
from main import create_airport
from messages import Messages

# TODO Change tests from Airplane (i changed capacity to seats based on ticket type)

@pytest.fixture
def airport():
    return create_airport()


def test_airplane_capacity(airport):
    for passenger_group in airport.passenger_groups:
        suitable_airplanes = airport.find_airplanes_for_passenger_group(passenger_group)
        if suitable_airplanes:
            chosen_airplane = suitable_airplanes[0]
            assert passenger_group.size <= chosen_airplane.capacity, Messages.PASSENGER_GROUP_CAPACITY_EXCEEDED.format(group_id=passenger_group.group_id)


def test_flight_dates(airport):
    for flight in airport.flights:
        assert flight.departure_time < flight.return_time, Messages.FLIGHT_RETURN_DATE_INVALID.format(flight_id=flight.flight_id)


def test_find_airplanes_for_passenger_group(airport):
    for passenger_group in airport.passenger_groups:
        suitable_airplanes = airport.find_airplanes_for_passenger_group(passenger_group)
        assert suitable_airplanes, Messages.NO_SUITABLE_AIRPLANE.format(group_id=passenger_group.group_id)
