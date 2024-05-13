from generator import Generator
import random 
from TicketCost import TicketCost
from Ticket import TicketType
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
        self.n_iterations = 100
        self.n_scouts = scouts
        self.n_best_sites = 10
        self.n_elites = 5
        self.n_recruited_elites = 5
        self.n_rectruited_best = 3
        
    # old solution
    def bees_algorithm_old(self,population, data_dict, fitness_values) -> tuple:
        """
        Perform a cycle of the Bees Algorithm.
        """
        n_iterations = 100
        n_elite_bees = 10 # TODO change interpretation
        n_sites = 5 # TODO change interpretation
        n_recruited_bees = 3  # example value
        n_remaining_bees = 5  # example value

        for _ in range(n_iterations):

            # Select the elite bees
            sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)
            # elite_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)[:n_elite_bees]
            elite_indices = sorted_indices[:n_elite_bees]
            elite_bees = [population[i] for i in elite_indices]

            # Select sites for neighborhood search
            sites = elite_bees[:n_sites]

            # Recruit bees around sites and evaluate their fitness TODO also for the rest of the sites/elite bees
            # fittest_bees = {}
            for site in sites:
                fittest_bee = None
                fittest_bee_fitness = None
                site_bees = []  # List to store the bees for the site
                for _ in range(n_recruited_bees):
                    # Generate a new solution in the neighborhood of the site
                    new_solution = Bees.generate_new_solution(site, data_dict)  # You need to implement this function

                    # Add the new solution to the site bees
                    site_bees.append(new_solution)

                    # Evaluate the fitness of the new solution
                    new_solution_fitness = Bees.evaluate_population([new_solution])[0]

                    # If the new solution is fitter than the current fittest bee for the site, update the fittest bee
                    if fittest_bee is None or new_solution_fitness > fittest_bee_fitness:
                        fittest_bee = new_solution
                        fittest_bee_fitness = new_solution_fitness

                # Store the fittest bee for the site
                # fittest_bees[site['id']] = fittest_bee

                # Add the fittest bee to the population
                population.append(fittest_bee) # TODO instead of adding change the population (replace)

            # Now, the population only contains the fittest bee from each site

            # Select the remaining bees
            remaining_bees = sorted_indices[n_elite_bees:]
            
            # Generate completely new solutions for the remaining bees
            new_population = Bees.generate_population(data_dict, n_remaining_bees)  # You need to implement this function
            # new_population = Bees.initialise_population(data_dict, len(population) - n_elite_bees)
            # Add the new population to the remaining bees
            for bee in new_population:
                population.append(bee) # TODO instead of adding change the remaining bees (replace)

            # Evaluate the population
            fitness_values = Bees.evaluate_population(population)

        return population, fitness_values
    
    @staticmethod
    def generate_population(data_dict: dict, population_size: int) -> list:
        """
        Get random solutions based on number of bees.
        """
        airplanes = data_dict["airplanes"]
        passenger_groups = data_dict["passenger_groups"]
        population = []

        for _ in range(population_size):
            solution = {airplane_id: {"groups": [], "destination": None, "free_seats": airplane.copy()} for airplane_id, airplane in airplanes.items()}
            for group_id, group in passenger_groups.items():
                suitable_airplanes = [a_id for a_id in airplanes.keys() if solution[a_id]["free_seats"][group["ticket_type"]] >= group["size"] and
                                        (solution[a_id]["destination"] is None or 
                                         solution[a_id]["destination"] == group["destination"])]
                if suitable_airplanes:
                    airplane_id = random.choice(suitable_airplanes)
                    solution[airplane_id]["groups"].append(group_id)
                    solution[airplane_id]["free_seats"][group["ticket_type"]] -= group["size"]
                    if solution[airplane_id]["destination"] is None:
                        solution[airplane_id]["destination"] = group["destination"] # First destination assigned (could be random in the beginning)
            population.append(solution)

        return population
    
    @staticmethod
    def evaluate_solution(solution: dict, data_dict: dict) -> int:
        """
        Evaluate the fitness of a solution.
        """
        total_revenue = 0
        total_costs = 0
        for airplane,data in solution.items():
            if data["groups"]:
                total_revenue += sum([TicketCost.get_ticket_cost(data_dict["passenger_groups"][group_id]["ticket_type"]) * data_dict["passenger_groups"][group_id]["size"] for group_id in data["groups"]])
        return total_revenue - total_costs
    
    @staticmethod
    def evaluate_population(population: list, data_dict: dict) -> list:
        """
        Evaluate the fitness of the population.
        """
        fitness_values = []
        PASSENGER_COST = 20 #TODO calculate passenger cost, probably move to evaluate_solution
        for solution in population:
            fitness_values.append(Bees.evaluate_solution(solution, data_dict))
        return fitness_values
    
    @staticmethod
    def generate_new_solution(site: dict, data_dict: dict) -> dict:
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
        unassigned_groups = [group for group in data_dict["passenger_groups"] if group not in all_assigned_group_ids]

        # If there are no unassigned groups, return the original solution
        if not unassigned_groups:
            return new_solution

        # Choose a new group for the airplane
        new_group, n_attempts = None, 10
        for _ in range(n_attempts):
            tmp_group = random.choice(unassigned_groups)
            if new_solution[airplane_to_change]["free_seats"][data_dict["passenger_groups"][tmp_group]["ticket_type"]] >= \
                data_dict["passenger_groups"][tmp_group]["size"] and new_solution[airplane_to_change]["destination"] == data_dict["passenger_groups"][tmp_group]["destination"]:
                new_group = tmp_group
                break

        # If no suitable group was found, return the original solution
        if new_group is None:
            return new_solution

        # Change the group in the new solution
        new_solution[airplane_to_change]["free_seats"][data_dict["passenger_groups"][group_to_change]["ticket_type"]] += data_dict["passenger_groups"][group_to_change]["size"]
        new_solution[airplane_to_change]["free_seats"][data_dict["passenger_groups"][new_group]["ticket_type"]] -= data_dict["passenger_groups"][new_group]["size"]
        new_solution[airplane_to_change]["groups"].remove(group_to_change)
        new_solution[airplane_to_change]["groups"].append(new_group)

        return new_solution

    def perform_local_search(indices: list, n_recruited: int, initial_population: list, data_dict: dict):
        """
        Perform local search around the fittest bees.
        This could be better optimized based on flower patch (Neighborhood shrinking and Site abandonment) - http://beesalgorithmsite.altervista.org/BeesAlgorithm.htm
        """
        for index in indices:
            fittest_bee = None
            fittest_bee_fitness = Bees.evaluate_solution(initial_population[index], data_dict)
            for _ in range(n_recruited):
                new_solution = Bees.generate_new_solution(initial_population[index], data_dict)
                new_solution_fitness = Bees.evaluate_solution(new_solution, data_dict)
                if new_solution_fitness > fittest_bee_fitness:
                    fittest_bee = new_solution
                    fittest_bee_fitness = new_solution_fitness

            if fittest_bee:
                initial_population[index] = fittest_bee

    def bees_cycle(self, data_dict: dict, initial_population: list, initial_fitness_values: list) -> tuple:
        """
        Perform a cycle of the Bees Algorithm.
        """
        population = deepcopy(initial_population)
        fitness_values = deepcopy(initial_fitness_values)

        for _ in range(self.n_iterations):

            sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)
            elite_indices = sorted_indices[:self.n_elites]
            remaining_best_indices = sorted_indices[self.n_elites:self.n_best_sites]

            # local search
            Bees.perform_local_search(elite_indices, self.n_recruited_elites, population, data_dict)
            Bees.perform_local_search(remaining_best_indices, self.n_rectruited_best, population, data_dict)

            # global search
            remaining_indices = sorted_indices[self.n_best_sites:]
            new_population = Bees.generate_population(data_dict, self.n_scouts - self.n_best_sites)
            for i, index in enumerate(remaining_indices):
                population[index] = new_population[i]
            
            fitness_values = Bees.evaluate_population(population, data_dict)

        return population, fitness_values

    def bees_algorithm(self, data_dict: dict) -> tuple:
        """
        Perform the Bees Algorithm.
        """
        # Generate initial population
        initial_population = Bees.generate_population(data_dict, self.n_scouts)
        
        # Evaluate the initial population (waggle dance)
        fitness_values = Bees.evaluate_population(initial_population, data_dict)

        # Select old best solution
        fitness_old, old_solution = None, None
        for fitness, solution in sorted(zip(fitness_values, initial_population), key=lambda x: x[0], reverse=True)[:1]:
            fitness_old, old_solution = fitness, solution

        # Perform a cycle of the Bees Algorithm
        last_population, fitness_values = self.bees_cycle(data_dict, initial_population, fitness_values)

        # Select new best solution
        fitness_new, new_solution = None, None
        for fitness, solution in sorted(zip(fitness_values, last_population), key=lambda x: x[0], reverse=True)[:1]:
            fitness_new, new_solution = fitness, solution
        
        # Check if fitness improved
        if fitness_old > fitness_new:
            assert False, f"Fitness did not improve: {fitness_old} > {fitness_new}"
        else:
            print(f"Fitness improved: {fitness_old} < {fitness_new}, improved by {fitness_new - fitness_old}")

        return new_solution,last_population

        
if __name__ == "__main__":
    for i in range(1):
        print(f"Test {i}")
        data_dict = Generator.generate_random_test_data(10, 100, 10)
        # Generator.print_data_dict(data_dict)

        bees = Bees(20)

        for _ in range(5):
            solution, population = bees.bees_algorithm(data_dict)
            # print(Bees.evaluate_solution(solution))



    
    
