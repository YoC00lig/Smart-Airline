from generator import Generator
import random 
from TicketCost import TicketCost
from Ticket import TicketType

# Example output:
# Airplanes:
# {'id': 'A1', 'seats': {<TicketType.FIRST_CLASS: 'First Class'>: 30, <TicketType.BUSINESS: 'Business Class'>: 60, <TicketType.ECONOMY: 'Economy Class'>: 180}}
# {'id': 'A2', 'seats': {<TicketType.FIRST_CLASS: 'First Class'>: 10, <TicketType.BUSINESS: 'Business Class'>: 90, <TicketType.ECONOMY: 'Economy Class'>: 130}}

# Passenger Groups:
# {'id': 'G1', 'size': 19, 'ticket_type': <TicketType.BUSINESS: 'Business Class'>, 'destination': 'Airport3', 'flight_date': datetime.date(2024, 4, 30)}
# {'id': 'G2', 'size': 12, 'ticket_type': <TicketType.BUSINESS: 'Business Class'>, 'destination': 'Airport3', 'flight_date': datetime.date(2024, 5, 3)}

class Bees:
    """
    Swarm Intelligence Algorithm - Bees Algorithm
    """

    @staticmethod
    def initialise_population(data_dict: dict, population_size: int):
        """
        Initialise the population with random solutions.
        """
        airplanes = data_dict["airplanes"]
        passenger_groups = data_dict["passenger_groups"]
        population = []

        for _ in range(population_size):
            solution = {airplane["id"]: {"groups": [], "destination": None} for airplane in airplanes}
            airplane_seats = {airplane["id"]: airplane["seats"].copy() for airplane in airplanes}
            for group in passenger_groups:
                suitable_airplanes = [a for a in airplanes if airplane_seats[a["id"]][group["ticket_type"]] >= group["size"] and 
                                      (solution[a["id"]]["destination"] is None or 
                                       solution[a["id"]]["destination"] == group["destination"])]
                if suitable_airplanes:
                    airplane = random.choice(suitable_airplanes)
                    solution[airplane["id"]]["groups"].append(group)
                    airplane_seats[airplane["id"]][group["ticket_type"]] -= group["size"]
                    if solution[airplane["id"]]["destination"] is None:
                        solution[airplane["id"]]["destination"] = group["destination"]
            population.append(solution)

        return population
    
    @staticmethod
    def evaluate_population(population):
        """
        Evaluate the fitness of the population.
        """
        fitness_values = []
        PASSENGER_COST = 20 #TODO calculate passenger cost
        for solution in population:
            total_revenue = 0
            total_costs = 0 #TODO calculate total costs
            for airplane,data in solution.items():
                if data["groups"]:
                    total_revenue += sum([TicketCost.get_ticket_cost(group["ticket_type"]) * group["size"] for group in data["groups"]])
            fitness_values.append(total_revenue - total_costs)
        return fitness_values
    @staticmethod
    def generate_new_solution(site, data_dict):
        """
        Generate a new solution in the neighborhood of the site.
        """
        # Create a copy of the site to avoid modifying the original solution
        new_solution = site.copy()

        # Choose an airplane to change
        airplane_to_change = random.choice(list(new_solution.keys()))

        # Choose a group to change in the airplane
        if new_solution[airplane_to_change]["groups"]:  # if there are groups assigned to the airplane
            group_to_change = random.choice(new_solution[airplane_to_change]["groups"])
        else:
            return new_solution  # if there are no groups assigned to the airplane, return the original solution

        # Get a list of all groups currently assigned to airplanes
        all_assigned_groups = [group for airplane in new_solution.values() for group in airplane["groups"]]

        # print("All Assigned Groups")
        # print(len(all_assigned_groups))
        # Get a list of all groups that are not currently assigned to any airplane
        unassigned_groups = [group for group in data_dict["passenger_groups"] if group not in all_assigned_groups]
        
        # print("Unassigned Groups")
        # print(len(unassigned_groups))
        # If there are no unassigned groups, return the original solution
        if not unassigned_groups:
            return new_solution

        # Choose a new group for the airplane
        new_group = random.choice(unassigned_groups)

        # Change the group in the new solution
        new_solution[airplane_to_change]["groups"].remove(group_to_change)
        new_solution[airplane_to_change]["groups"].append(new_group)

        return new_solution

    
    
    @staticmethod
    def bees_cycle(population, data_dict, fitness_values):
        """
        Perform a cycle of the Bees Algorithm.
        """
        n_iterations = 100
        n_elite_bees = 10
        n_sites = 5
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

            # Recruit bees around sites and evaluate their fitness
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
                    new_solution_fitness = Bees.evaluate_population([new_solution])

                    # If the new solution is fitter than the current fittest bee for the site, update the fittest bee
                    if fittest_bee is None or new_solution_fitness > fittest_bee_fitness:
                        fittest_bee = new_solution
                        fittest_bee_fitness = new_solution_fitness

                # Store the fittest bee for the site
                # fittest_bees[site['id']] = fittest_bee

                # Add the fittest bee to the population
                population.append(fittest_bee)

            # Now, the population only contains the fittest bee from each site

            # Select the remaining bees
            remaining_bees = sorted_indices[n_elite_bees:]
            
            # Generate completely new solutions for the remaining bees
            new_population = Bees.initialise_population(data_dict, n_remaining_bees)  # You need to implement this function
            # new_population = Bees.initialise_population(data_dict, len(population) - n_elite_bees)
            # Add the new population to the remaining bees
            for bee in new_population:
                population.append(bee)

            # Evaluate the population
            fitness_values = Bees.evaluate_population(population)

        return population, fitness_values



        
    
if __name__ == "__main__":
    data_dict = Generator.generate_random_test_data(3, 100, 3)
    Generator.print_data_dict(data_dict)

    population = Bees.initialise_population(data_dict, 5)
    print("Population:")
    for solution in population:
        for airplane, groups in solution.items():
            print(f"Airplane: {airplane}, Destination: {groups['destination']}")
            print("Groups:")
            for group in groups["groups"]:
                print(group)
        print("\n")

    fitness_values = Bees.evaluate_population(population)
    print("Fitness Values:")
    for fitness in fitness_values:
        print(fitness)

    new_population, new_fitness_values = Bees.bees_cycle(population, data_dict, fitness_values)

    print("New Population:")
    # ...

    print("New Fitness Values:")
    for fitness in sorted(new_fitness_values, reverse=True)[:10]:
        print(fitness)



    
    
