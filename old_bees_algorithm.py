from algorithm import Bees


def bees_algorithm_old(population, data_dict, fitness_values) -> tuple:
    """
    Perform a cycle of the Bees Algorithm.
    """
    n_iterations = 100
    n_elite_bees = 10
    n_sites = 5
    n_recruited_bees = 3
    n_remaining_bees = 5

    for _ in range(n_iterations):

        # Select the elite bees
        sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i], reverse=True)
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
