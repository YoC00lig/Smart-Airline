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
        self.airplanes = data_dict['airplanes']
        self.passenger_groups = data_dict['passenger_groups']

        # Generate initial population
        initial_population = self.generate_population(self.number_of_scouts)

        # Evaluate the initial population (waggle dance)
        fitness_values = self.evaluate_population(initial_population)

        # Select old best solution
        fitness_old, old_solution = None, None
        for fitness, solution in sorted(zip(fitness_values, initial_population), key=lambda x: x[0], reverse=True)[:1]:
            fitness_old, old_solution = fitness, solution

        # Perform a cycle of the Bees Algorithm
        last_population, fitness_values = self.bees_cycle(initial_population, fitness_values)

        # Select new best solution
        fitness_new, new_solution = None, None
        for fitness, solution in sorted(zip(fitness_values, last_population), key=lambda x: x[0], reverse=True)[:1]:
            fitness_new, new_solution = fitness, solution

        # Check if fitness improved
        if fitness_old > fitness_new:
            assert False, f"Fitness did not improve: {fitness_old} > {fitness_new}"
        else:
            print(f"Fitness improved: {fitness_old} < {fitness_new}, improved by {fitness_new - fitness_old}")

        return new_solution, last_population

    def generate_population(self, population_size: int) -> list:
        """
        Get random solutions based on number of bees.
        """
        # airplanes = data_dict["airplanes"]
        # passenger_groups = data_dict["passenger_groups"]
        population = []

        for _ in range(population_size):
            solution = {
                airplane_id: {"groups": [], "destination": None, "free_seats": airplane.copy()}
                for airplane_id, airplane in self.airplanes.items()
            }
            for group_id, group in self.passenger_groups.items():
                suitable_airplanes = [
                    a_id for a_id in self.airplanes.keys()
                    if solution[a_id]["free_seats"][group["ticket_type"]] >= group["size"] and
                    (solution[a_id]["destination"] is None or
                     solution[a_id]["destination"] == group["destination"])
                ]
                if suitable_airplanes:
                    airplane_id = random.choice(suitable_airplanes)
                    solution[airplane_id]["groups"].append(group_id)
                    solution[airplane_id]["free_seats"][group["ticket_type"]] -= group["size"]
                    if solution[airplane_id]["destination"] is None:
                        solution[airplane_id]["destination"] = group["destination"] # First destination assigned (could be random in the beginning)
            population.append(solution)

        return population

    def evaluate_solution(self, solution: dict) -> int:
        """
        Evaluate the fitness of a solution.
        """
        total_revenue = 0
        total_costs = 0
        for airplane, data in solution.items():
            for group_id in data["groups"]:
                ticket_type = self.passenger_groups[group_id]["ticket_type"]
                ticket_cost = TicketCost.get_ticket_cost(ticket_type)
                size = self.passenger_groups[group_id]["size"]
                total_revenue += ticket_cost * size

        return total_revenue - total_costs

    def evaluate_population(self, population: list) -> list:
        """
        Evaluate the fitness of the population.
        """
        fitness_values = []
        PASSENGER_COST = 20 #TODO calculate passenger cost, probably move to evaluate_solution
        for solution in population:
            fitness_values.append(self.evaluate_solution(solution))
        return fitness_values

    def generate_new_solution(self, site: dict) -> dict:
        """
        Generate a new solution in the neighborhood of the site.
        """
        # Create a copy of the site to avoid modifying the original solution
        new_solution = deepcopy(site)

        # Choose an airplane to change
        airplane_to_change = random.choice(list(new_solution.keys()))

        # Choose a group to change in the airplane
        group_to_change = None
        if new_solution[airplane_to_change]["groups"]:  # if there are groups assigned to the airplane
            group_to_change = random.choice(new_solution[airplane_to_change]["groups"])
        else:
            return new_solution  # if there are no groups assigned to the airplane, return the original solution

        # Get a set of all group IDs currently assigned to airplanes
        all_assigned_group_ids = {group for airplane in new_solution.values() for group in airplane["groups"]}

        # Get a list of all groups that are not currently assigned to any airplane
        unassigned_groups = [group for group in self.passenger_groups if group not in all_assigned_group_ids]

        # If there are no unassigned groups, return the original solution
        if not unassigned_groups:
            return new_solution

        # Choose a new group for the airplane
        new_group, n_attempts = None, 10
        for _ in range(n_attempts):
            tmp_group = random.choice(unassigned_groups)
            if (new_solution[airplane_to_change]["free_seats"][self.passenger_groups[tmp_group]["ticket_type"]] >=
                    self.passenger_groups[tmp_group]["size"] and new_solution[airplane_to_change]["destination"] ==
                    self.passenger_groups[tmp_group]["destination"]):
                new_group = tmp_group
                break

        # If no suitable group was found, return the original solution
        if new_group is None:
            return new_solution

        # Change the group in the new solution
        new_solution[airplane_to_change]["free_seats"][self.passenger_groups[group_to_change]["ticket_type"]] += self.passenger_groups[group_to_change]["size"]
        new_solution[airplane_to_change]["free_seats"][self.passenger_groups[new_group]["ticket_type"]] -= self.passenger_groups[new_group]["size"]
        new_solution[airplane_to_change]["groups"].remove(group_to_change)
        new_solution[airplane_to_change]["groups"].append(new_group)

        return new_solution

    def perform_local_search(self, indices: list, n_recruited: int, initial_population: list):
        """
        Perform local search around the fittest bees.
        This could be better optimized based on flower patch (Neighborhood shrinking and Site abandonment) - http://beesalgorithmsite.altervista.org/BeesAlgorithm.htm
        """
        for index in indices:
            fittest_bee = None
            fittest_bee_fitness = self.evaluate_solution(initial_population[index])
            for _ in range(n_recruited):
                new_solution = self.generate_new_solution(initial_population[index])
                new_solution_fitness = self.evaluate_solution(new_solution)
                if new_solution_fitness > fittest_bee_fitness:
                    fittest_bee = new_solution
                    fittest_bee_fitness = new_solution_fitness

            if fittest_bee:
                initial_population[index] = fittest_bee

    def bees_cycle(self, initial_population: list, initial_fitness_values: list) -> tuple:
        """
        Perform a cycle of the Bees Algorithm.
        """
        population = deepcopy(initial_population)
        fitness_values = deepcopy(initial_fitness_values)

        for _ in range(self.number_of_iterations):

            sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)
            elite_indices = sorted_indices[:self.number_of_elites]
            remaining_best_indices = sorted_indices[self.number_of_elites:self.number_of_best_sites]

            # local search
            self.perform_local_search(elite_indices, self.number_of_recruited_elites, population)
            self.perform_local_search(remaining_best_indices, self.number_of_recruited_best, population)

            # global search
            remaining_indices = sorted_indices[self.number_of_best_sites:]
            new_population = self.generate_population(self.number_of_scouts - self.number_of_best_sites)
            for i, index in enumerate(remaining_indices):
                population[index] = new_population[i]
            
            fitness_values = self.evaluate_population(population)

        return population, fitness_values

        
if __name__ == "__main__":
    for i in range(1):
        print(f"Test {i}")
        data = Generator.generate_random_test_data(
            10,
            100,
            10
        )
        # Generator.print_test_data(data)

        bees = Bees(20)

        for _ in range(5):
            solution, population = bees.bees_algorithm(data)
            # print(Bees.evaluate_solution(solution))
