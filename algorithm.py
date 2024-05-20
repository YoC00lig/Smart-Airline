from generator import Generator
import random 
from TicketCost import TicketCost
from copy import deepcopy

# Example input:
# Airplanes:
# {'A1': {'seats': {<TicketType.FIRST_CLASS: 'First Class'>: 30, <TicketType.BUSINESS: 'Business Class'>: 60, <TicketType.ECONOMY: 'Economy Class'>: 180}}}
# {'A2': {'seats': {<TicketType.FIRST_CLASS: 'First Class'>: 10, <TicketType.BUSINESS: 'Business Class'>: 90, <TicketType.ECONOMY: 'Economy Class'>: 130}}}

# Passenger Groups:
# {'G1': {size': 19, 'ticket_type': <TicketType.BUSINESS: 'Business Class'>, 'destination': 'Airport3', 'flight_date': datetime.date(2024, 4, 30)}}
# {'G2': {'size': 12, 'ticket_type': <TicketType.BUSINESS: 'Business Class'>, 'destination': 'Airport3', 'flight_date': datetime.date(2024, 5, 3)}}


class Bees:
    """
    Swarm Intelligence Algorithm - Bees Algorithm
    """
    def __init__(self, scouts: int):
        self.number_of_scouts = scouts
        self.number_of_iterations = 100
        self.number_of_best_sites = 10
        self.number_of_elites = 5
        self.number_of_recruited_elites = 5
        self.number_of_recruited_best = 3
        self.airplanes = None
        self.passenger_groups = None

    def bees_algorithm(self, data_dict: dict) -> tuple:
        """
        Perform the Bees Algorithm.
        """
        # Save values from data dict in class object
        self.airplanes = data_dict['airplanes']
        self.passenger_groups = data_dict['passenger_groups']

        # Generate initial population
        initial_population = self.generate_population(self.number_of_scouts)

        # Evaluate the initial population (waggle dance)
        fitness_values = self.evaluate_population(initial_population)

        # Select old best solution
        fitness_old, old_solution = Bees.get_best_solution_sorted_by_fitness_value(initial_population, fitness_values)

        # Perform a cycle of the Bees Algorithm
        last_population, fitness_values = self.bees_cycle(initial_population, fitness_values)

        # Select new best solution
        fitness_new, new_solution = Bees.get_best_solution_sorted_by_fitness_value(last_population, fitness_values)

        # Check if fitness improved
        self.has_fitness_improved(fitness_old, fitness_new)

        return new_solution, last_population

    def generate_population(self, population_size: int) -> list:
        """
        Get random solutions based on number of bees.
        """
        return [self.generate_random_solution() for _ in range(population_size)]

    def generate_random_solution(self) -> dict:
        solution = {
            airplane_id: {"groups": [], "destination": None, "free_seats": airplane.copy()}
            for airplane_id, airplane in self.airplanes.items()
        }
        for group_id, group in self.passenger_groups.items():
            suitable_airplanes = self.get_suitable_airplanes(group, solution)
            if suitable_airplanes:
                airplane_id = random.choice(suitable_airplanes)
                solution[airplane_id]["groups"].append(group_id)
                solution[airplane_id]["free_seats"][group["ticket_type"]] -= group["size"]
                if solution[airplane_id]["destination"] is None:
                    # First destination assigned (could be random in the beginning)
                    solution[airplane_id]["destination"] = group["destination"]
        return solution

    def get_suitable_airplanes(self, group: dict, solution: dict) -> list:
        return [
                    airplane_id for airplane_id in self.airplanes.keys()
                    if self.has_enough_space(solution[airplane_id], group) and
                    self.has_correct_destination(solution[airplane_id], group)
                ]

    @staticmethod
    def has_enough_space(airplane, group):
        return airplane["free_seats"][group["ticket_type"]] >= group["size"]

    @staticmethod
    def has_correct_destination(airplane, group):
        return airplane["destination"] is None or airplane["destination"] == group["destination"]

    def evaluate_population(self, population: list) -> list:
        """
        Evaluate the fitness of the population.
        """
        return [self.evaluate_solution(solution) for solution in population]

    def evaluate_solution(self, solution: dict) -> int:
        """
        Evaluate the fitness of a solution.
        """
        PASSENGER_COST = 20  # TODO calculate passenger cost
        total_revenue = 0
        total_costs = 0
        for airplane, data in solution.items():
            for group_id in data["groups"]:
                ticket_type = self.passenger_groups[group_id]["ticket_type"]
                ticket_cost = TicketCost.get_ticket_cost(ticket_type)
                size = self.passenger_groups[group_id]["size"]
                total_revenue += ticket_cost * size

        return total_revenue - total_costs

    def bees_cycle(self, initial_population: list, initial_fitness_values: list) -> tuple:
        """
        Perform a cycle of the Bees Algorithm.
        """
        population = deepcopy(initial_population)
        fitness_values = deepcopy(initial_fitness_values)

        for _ in range(self.number_of_iterations):
            elite_indices, remaining_best_indices, remaining_indices = self.separate_indices(fitness_values)

            # local search
            self.perform_local_search(elite_indices, self.number_of_recruited_elites, population)
            self.perform_local_search(remaining_best_indices, self.number_of_recruited_best, population)

            # global search
            new_population = self.generate_population(self.number_of_scouts - self.number_of_best_sites)
            for i, index in enumerate(remaining_indices):
                population[index] = new_population[i]

            fitness_values = self.evaluate_population(population)

        return population, fitness_values

    def separate_indices(self, fitness_values: list) -> tuple:
        sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)
        elite_indices = sorted_indices[:self.number_of_elites]
        remaining_best_indices = sorted_indices[self.number_of_elites:self.number_of_best_sites]
        remaining_indices = sorted_indices[self.number_of_best_sites:]
        return elite_indices, remaining_best_indices, remaining_indices

    def perform_local_search(self, bees_indices: list, number_of_recruited_bees: int, population: list):
        """
        Perform local search around the fittest bees.
        This could be better optimized based on flower patch (Neighborhood shrinking and Site abandonment) - http://beesalgorithmsite.altervista.org/BeesAlgorithm.htm
        """
        for bee_index in bees_indices:
            fittest_bee_fitness = self.evaluate_solution(population[bee_index])

            for _ in range(number_of_recruited_bees):
                new_solution = self.generate_new_solution(population[bee_index])
                new_solution_fitness = self.evaluate_solution(new_solution)
                if new_solution_fitness > fittest_bee_fitness:
                    fittest_bee_fitness = new_solution_fitness
                    population[bee_index] = new_solution

    def generate_new_solution(self, site: dict) -> dict:
        """
        Generate a new solution in the neighborhood of the site.
        """
        # Create a copy of the site to avoid modifying the original solution
        new_solution = deepcopy(site)
        airplane_id_to_change = Bees.choose_random_airplane_with_groups(new_solution)

        # if there are no airplanes with groups
        if not airplane_id_to_change:
            return new_solution

        airplane_groups = new_solution[airplane_id_to_change]["groups"]
        old_group = random.choice(airplane_groups)

        new_group = self.choose_new_group_for_the_airplane(new_solution, new_solution[airplane_id_to_change])
        # If no suitable group was found, return the original solution
        if new_group is None:
            return new_solution

        new_solution = self.update_new_solution(old_group, new_group, airplane_id_to_change, new_solution)

        return new_solution

    @staticmethod
    def choose_random_airplane_with_groups(solution: dict) -> str | None:
        airplanes = list(solution.items())
        airplanes_with_groups = list(filter(lambda airplane: len(airplane[1]["groups"]) >= 1, airplanes))
        # if there is no airplane with groups
        if not airplanes_with_groups:
            return None

        random_airplane = random.choice(airplanes_with_groups)
        return random_airplane[0]

    def choose_new_group_for_the_airplane(
            self, solution: dict, airplane: dict, number_of_attempts: int = 10
    ) -> dict | None:

        unassigned_groups = self.get_unassigned_groups(solution)
        if not unassigned_groups:
            return None

        new_group = None

        for _ in range(number_of_attempts):
            random_group_id = random.choice(unassigned_groups)
            random_group = self.passenger_groups[random_group_id]
            if (
                Bees.has_enough_space(airplane, random_group) and
                Bees.has_correct_destination(airplane, random_group)
            ):
                new_group = random_group
                break

        return new_group

    def get_unassigned_groups(self, solution: dict) -> list:
        all_assigned_group_ids = {group for airplane in solution.values() for group in airplane["groups"]}
        # Get a list of all groups that are not currently assigned to any airplane
        unassigned_groups = [group for group in self.passenger_groups if group not in all_assigned_group_ids]
        return unassigned_groups

    def update_new_solution(self, old_group, new_group, airplane_id_to_change, new_solution: dict) -> dict:
        old_group_ticket_type = self.passenger_groups[old_group]["ticket_type"]
        new_group_ticket_type = self.passenger_groups[new_group]["ticket_type"]

        # Remove old group
        new_solution[airplane_id_to_change]["free_seats"][old_group_ticket_type] += (
            self.passenger_groups)[old_group]["size"]
        new_solution[airplane_id_to_change]["groups"].remove(old_group)

        # Add new group
        new_solution[airplane_id_to_change]["free_seats"][new_group_ticket_type] -= (
            self.passenger_groups)[new_group]["size"]
        new_solution[airplane_id_to_change]["groups"].append(new_group)
        return new_solution

    @staticmethod
    def get_best_solution_sorted_by_fitness_value(population: list, fitness_values: list) -> any:
        sorted_population = sorted(zip(fitness_values, population), key=lambda x: x[0], reverse=True)
        if sorted_population:
            return sorted_population[0]
        else:
            return None, None

    @staticmethod
    def has_fitness_improved(fitness_old: int, fitness_new: int) -> None:
        if fitness_old > fitness_new:
            print(f"Fitness did not improve: {fitness_old} > {fitness_new}")
        else:
            print(f"Fitness improved: {fitness_old} < {fitness_new}, improved by {fitness_new - fitness_old}")

        
if __name__ == "__main__":
    data = Generator.generate_random_test_data(
        10,
        100,
        10
    )
    # Generator.print_test_data(data)

    bees = Bees(20)

    for _ in range(5):
        final_solution, final_population = bees.bees_algorithm(data)
        # print(Bees.evaluate_solution(solution))
