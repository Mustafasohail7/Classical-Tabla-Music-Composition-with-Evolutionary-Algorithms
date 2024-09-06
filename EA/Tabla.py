import random 
import math
import numpy as np
from problem import Problem

class Tabla(Problem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_good_pairs = kwargs.get('good_pairs', [])
        self.max_good_pairs = self.calculate_max_good_pairs()
        self.ideal_tempo = 200
        self.max_diversity_index = ((self.population_size - 1) * self.length) // 2

        # weights
        self.tempo_weight = 0.4
        self.pairs_weight = 0.4
        self.diversity_weight = 0.2

    def calculate_fitness(self, chromosome):
        """
        Function to calculate the fitness of a chromosome
        """
        # Individual contributions to fitness
        tempo_fitness = self.calculate_tempo(chromosome[0])

        good_pairs = self.check_good_pairs(chromosome[0])
        repetition_penalty = self.calculate_dynamic_repetition_penalty(chromosome[0])
        good_pairs -= repetition_penalty

        diversity_index = self.calculate_shared_fitness(chromosome, self.population)

        # Normalize the values
        normalized_tempo = math.exp(-((tempo_fitness - self.ideal_tempo) ** 2) / (2 * (self.ideal_tempo ** 2)))
        normalized_pairs = 1 - abs(good_pairs - self.max_good_pairs) / self.max_good_pairs
        normalized_diversity = math.exp(-((diversity_index) ** 2) / (2 * 0.3 * (self.max_diversity_index) ** 2))

        # weighted sum of the contributions
        tempo_part = self.tempo_weight * normalized_tempo
        pairs_part = self.pairs_weight * normalized_pairs
        diversity_part = self.diversity_weight * normalized_diversity
        fitness = max(0, (tempo_part + pairs_part + diversity_part) * 100)

        return fitness

    def crossover(self,parent1, parent2):
        '''
        Crossover function that takes two parents and returns two children
            Args:
                parent1 (tuple): A tuple containing the first parent chromosome and its fitness
                parent2 (tuple): A tuple containing the second parent chromosome and its fitness
            Returns:
                tuple: A tuple containing the first child chromosome and its fitness
                tuple: A tuple containing the second child chromosome and its fitness
        '''

        crossover_point = random.randint(1, self.length - 1)

        child1_solution = parent1[0][:crossover_point] + parent2[0][crossover_point:]
        child2_solution = parent2[0][:crossover_point] + parent1[0][crossover_point:]

        child1_fitness = self.calculate_fitness((child1_solution,0))
        child2_fitness = self.calculate_fitness((child2_solution,0))

        child1 = (child1_solution, child1_fitness)
        child2 = (child2_solution, child2_fitness)

        return child1, child2

    def mutate(self, chromosome):
        '''
        Mutation function that takes a chromosome and returns a mutated chromosome
            Args:
                chromosome (tuple): A tuple containing the chromosome and its fitness
            Returns:
                tuple: A tuple containing the mutated chromosome and its fitness
        '''

        mutated_chromosome = list(chromosome[0])
        max_shift = 200  

        # interval mutation for tempo
        if random.random() < self.mutation_rate:
            index = random.randint(0, len(mutated_chromosome) - 1)
            shift = random.uniform(-max_shift, max_shift) 
            mutated_chromosome[index] = (
                mutated_chromosome[index][0],
                mutated_chromosome[index][1] + shift,
                self.mutate_volume(mutated_chromosome[index][2])
            )

        #swap mutation
        if random.random() < self.mutation_rate:
            i,j = random.sample(range(len(mutated_chromosome)),2)
            mutated_chromosome[i],mutated_chromosome[j] = mutated_chromosome[j],mutated_chromosome[i]

        #subsequence reverse mutation
        if random.random() < self.mutation_rate:
            i,j = sorted(random.sample(range(len(mutated_chromosome)),2))
            mutated_chromosome = mutated_chromosome[:i] + mutated_chromosome[i:j+1][::-1] + mutated_chromosome[j+1:]

        mutated_fitness = self.calculate_fitness((mutated_chromosome,0))
        
        return (mutated_chromosome, mutated_fitness)
    
    def mutate_volume(self, volume):
        '''
        Mutation function that applies a random noise to the volume and returns the mutated volume.  
            Args:
                volume (float): The original volume value to be mutated.
            
            Returns:
                float: The mutated volume value, constrained between -3 and 3.
        '''
        noise = np.random.uniform(-self.volume_mutation_range, self.volume_mutation_range)
        mutated_volume = volume + noise
        mutated_volume = max(-3, min(3, mutated_volume))
        return mutated_volume

    def random_chromosome(self):
        '''
        Generates a random chromosome composed of tabla sounds with random intervals and volumes.
            Args:
                None
            
            Returns:
                tuple: A tuple containing the generated chromosome (list of tuples with sound name, interval, and volume) and its initial fitness (set to 0.0).
        '''
        solution = []
        interval = 0
        total_time = 0
        for i in range(self.length):
            sound_name = random.choice(list(self.tabla_sounds.keys()))  
            volume_db = random.uniform(-3, 3)
            solution.append((sound_name, interval, volume_db))
            interval = random.uniform(0, 1500)
            total_time += interval
        chromosome = (solution, 0.0)
        return chromosome
    
    def get_repeated_sequences(self, chromosome):
        '''
        Identifies repeated sequences of the same bol (sound) in a chromosome and returns their details.
            Args:
                chromosome (list): A list of tuples representing the chromosome, where each tuple contains a bol (sound name), interval, and volume.
            
            Returns:
                list: A list of tuples, each containing the repeated bol, the length of the repetition, and the starting index of the sequence in the chromosome.
        '''
        sequence_info = []
        i = 0
        while i < len(chromosome):
            current_bol = chromosome[i][0]
            length = 1
            while i + 1 < len(chromosome) and chromosome[i + 1][0] == current_bol:
                length += 1
                i += 1
            if length > 1:
                sequence_info.append((current_bol, length, i - length + 1))
            i += 1
        return sequence_info
        
    def calculate_shared_fitness(self, chromosome, population):
        '''
        Calculates the shared fitness of a chromosome by comparing it with the rest of the population using Hamming distance.
            Args:
                chromosome (tuple): A tuple representing the chromosome, where the first element is a list of tuples (bol, interval, volume), and the second element is the fitness.
                population (list): A list of chromosomes, each represented as a tuple similar to the input chromosome.
            
            Returns:
                int: The sum of the Hamming distances between the given chromosome and the other chromosomes in the population.
        '''
        distances = 0
        for other in population:
            if chromosome != other:  # Avoid self-comparison
                a = self.hamming_distance(chromosome[0], other[0])
                distances += a
        return distances

    def calculate_dynamic_repetition_penalty(self, chromosome):
        '''
        Calculates a dynamic penalty based on the length of repeated sequences in the chromosome.
            Args:
                chromosome (list): A list of tuples representing the chromosome, where each tuple contains a bol (sound name), interval, and volume.
            
            Returns:
                int: The total penalty, calculated as the sum of the excess length over a defined repetition threshold for each repeated sequence.
        '''
        sequence_info = self.get_repeated_sequences(chromosome)
        total_penalty = 0
        repetition_threshold = 3

        for _, length, _ in sequence_info:
            if length > repetition_threshold:
                penalty = length - repetition_threshold
                total_penalty += penalty

        return total_penalty
    
    def calculate_max_good_pairs(self):
        # Calculate max_good_pairs based on the number of input good pairs
        num_input_pairs = len(self.input_good_pairs)
        base_max = self.length // 5 
        pairs_addition = num_input_pairs * (self.length // 50)
        return min(self.length//2,int(base_max + pairs_addition))
    
    def calculate_intervals(self,chromosome): 
        # Calculate the intervals between the tabla sounds in the chromosome 
        intervals = []
        for i in range(len(chromosome)):
            a = chromosome[i][1]
            intervals.append(a)
        return intervals

    def calculate_tempo(self, chromosome):
        # Calculate the tempo of the tabla chromosome
        intervals = self.calculate_intervals(chromosome)
        total_time = sum(intervals)
        avg_interval = total_time / (len(chromosome) - 1)
        return avg_interval
    
    def check_good_pair(self,sound1,sound2):   
        # Check if a pair of tabla sounds is a good pair   
        if (sound1,sound2) in self.good_pairs:             
            return True         
        return False      
    
    def check_good_pairs(self,chromosome): 
        # Check the number of good pairs in a tabla chromosome 
        count = 0         
        for i in range(1,len(chromosome)):             
            if self.check_good_pair(chromosome[i-1][0],chromosome[i][0]):                 
                count += 1        
        return count
    
    def hamming_distance(self,chromosome1, chromosome2):
        # Calculate the hamming distance between two tabla chromosomes
        return sum(c1[0] == c2[0] for c1, c2 in zip(chromosome1, chromosome2))