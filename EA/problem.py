import random
import numpy as np

class Problem():
    def __init__(self,population_size,offspring_size,generations,mutation_rate,iterations,length,data_folder,tabla_sounds,good_pairs):
        self.population_size = population_size
        self.offspring_size = offspring_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.iterations = iterations
        self.tournament_size = 2
        self.length = length
        self.volume_mutation_range = 2
        self.data_folder = data_folder
        self.tabla_sounds = tabla_sounds
        self.good_pairs = good_pairs
        self.data = self.read_file()
        self.init_population()
    
    def init_population(self):
        self.population = []  # Add this line to initialize the population attribute

        for _ in range(self.population_size):
            self.population.append(self.random_chromosome()) 
    
    def fitness_prop_selection(self, p=False, s=False):
        """
        Function to perform fitness proportionate selection
        """
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 

        fitness_values = []
        for x in self.population:
            if isinstance(x[1], tuple):
                fitness_values.append(x[1][0])  # Assuming the first element of the tuple is the fitness
            else:
                fitness_values.append(x[1])

        total_fitness = sum(fitness_values)
        probabilities = [x / total_fitness for x in fitness_values]

        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents

        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors
 
    def rank_based_selection(self, p=False, s=False):
        """
        Function to perform rank-based selection
        """
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        # Select two parents using rank-based selection
        fitness_sorted = sorted(self.population, key=lambda x: x[1])
        fitness_range = range(1, len(fitness_sorted) + 1)
        probabilities = [x / sum([y for y in fitness_range]) for x in reversed(fitness_range)]
        if p:
            choice = np.random.choice(range(len(self.population)), 2, p=probabilities, replace=False)
            parents = [self.population[choice[0]], self.population[choice[1]]]
            return parents
        if s:
            choice = np.random.choice(range(len(self.population)), self.population_size, p=probabilities, replace=False)
            survivors = [self.population[x] for x in choice]
            return survivors


    def truncation(self, p=False, s=False):
        if not p and not s:
            print("Specify whether to use the function for parent or survivor selection")
            return 
        if p:
            # Selects two parents using truncation selection
            parents = sorted(self.population, key=lambda x: x[1], reverse=True)[:2]
            return parents
        if s:
            # Selects survivors using truncation selection
            survivors = sorted(self.population, key=lambda x: x[1], reverse=True)[:self.population_size]
            return survivors

    def random(self,p=False,s=False):
        if not p and not s:
            print("Specify whether to use function for parent or survivor selection")
            return 
        
        if p:
            choice = [random.randint(1,self.population_size)-1 for i in range(2)]
            parents = [self.population[choice[0]],self.population[choice[1]]]
            return parents
        if s:
            choice = [random.randint(1,self.population_size)-1 for i in range(self.population_size)]
            survivors = [self.population[choice[i]] for i in choice]
            return survivors
        
    def calculate_fitness(self, chromosome):
        pass 

    def random_chromosome(self):
        pass

    def read_file(self):
        pass
