from Tabla import Tabla
from pydub import AudioSegment
import os

class EA: 
    def __init__(self, population_size, offspring_size, generations, mutation_rate, iterations, parent_selection_scheme, survivor_selection_scheme, length, good_pairs):
        self.parent_selection_scheme = parent_selection_scheme
        self.survivor_selection_scheme = survivor_selection_scheme
        self.data_folder = 'Data'
        self.tabla_sounds = {
            'DHA': AudioSegment.from_file(os.path.join(self.data_folder, 'DoubleHandedBols/DHA.wav'), format='wav'),
            'DHIN': AudioSegment.from_file(os.path.join(self.data_folder, 'DoubleHandedBols/DHIN.wav'), format='wav'),
            'GE': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/GE.wav'), format='wav'),
            'GHE': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/GHE.wav'), format='wav'),
            'KA': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/KA.wav'), format='wav'),
            'KAT': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/KAT.wav'), format='wav'),
            'TA': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TA.wav'), format='wav'),
            'TIN': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TIN.wav'), format='wav'),
            'TIT': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TIT.wav'), format='wav'),
            'TU': AudioSegment.from_file(os.path.join(self.data_folder, 'SingleHandedBols/TU.wav'), format='wav'), 
            # Additional 7 Bols
            'DHIT': AudioSegment.from_file(os.path.join(self.data_folder, 'DoubleHandedBols/DHIT.wav'), format='wav'),
            'GADIGEN': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/GADIGEN.wav'), format='wav'),
            'GHDASN': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/GHDASN.wav'), format='wav'),
            'KATIT': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/KATIT.wav'), format='wav'),
            'TIN-TENE': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/TIN-TENE.wav'), format='wav'),
            'TITT': AudioSegment.from_file(os.path.join(self.data_folder, 'CompoundBols/TITT.wav'), format='wav'),
        }
        self.length = length
        self.instance = Tabla(population_size, offspring_size, generations, mutation_rate, iterations, length, self.data_folder, self.tabla_sounds, good_pairs=good_pairs)
        self.iterations = iterations  

    def run(self):
        # Initialize variables to store high and low solutions
        high_solutions = []
        low_solutions = []
        generation_scores = []  

        parent_selection_function = getattr(self.instance, self.parent_selection_scheme)
        survivor_selection_function = getattr(self.instance, self.survivor_selection_scheme)

        if not callable(parent_selection_function) or not callable(survivor_selection_function):
            print("Invalid selection scheme")
            return

        self.iteration_scores = dict()

        for i in range(self.instance.iterations): # main loop
            high_solution_iteration = (None, float('-inf'))
            low_solution_iteration = (None, float('inf'))

            generation_scores = []

            # Initialize population
            self.instance.population = [self.instance.random_chromosome() for _ in range(self.instance.population_size)]

            for j in range(self.instance.generations):
                # Calculate fitness for the entire population
                self.instance.population = [(chrom[0], self.instance.calculate_fitness(chrom)) 
                                            for chrom in self.instance.population]

                generation_score = max(self.instance.population, key=lambda x: x[1])[1]
                generation_scores.append(generation_score)

                for k in range(0, self.instance.offspring_size, 2):
                    # Select parents and perform crossover
                    parents = parent_selection_function(p=True)
                    offspring1,offspring2 = self.instance.crossover(parents[0], parents[1])

                    # Mutate offspring
                    self.instance.population.append(self.instance.mutate(offspring1))
                    self.instance.population.append(self.instance.mutate(offspring2))

                survivors = survivor_selection_function(s=True)

                self.instance.population = survivors
                high_solution_generation = max(self.instance.population, key=lambda x: x[1])
                low_solution_generation = min(self.instance.population, key=lambda x: x[1])

                # Generate audio for the initial generation
                if j == 0 and i == 0:
                    self.generate_audio_from_chromosome(high_solution_generation[0]).export('initial.wav', format='wav')

                print(f"Iteration: {i+1}, Generation:{j+1}, High solution generation: ", high_solution_generation[1])

                if high_solution_generation[1] > high_solution_iteration[1]:
                    high_solution_iteration = high_solution_generation

                if low_solution_generation[1] < low_solution_iteration[1]:
                    low_solution_iteration = low_solution_generation

            high_solutions.append(high_solution_iteration)
            low_solutions.append(low_solution_iteration)

            self.iteration_scores[i] = generation_scores

        highest_solution = max(high_solutions, key=lambda x: x[1])
        lowest_solution = min(low_solutions, key=lambda x: x[1])

        self.generate_audio_from_chromosome(highest_solution[0]).export('good.wav', format='wav')
        self.generate_audio_from_chromosome(lowest_solution[0]).export('bad.wav', format='wav')

    def generate_audio_from_chromosome(self,chromosome):
        audio = AudioSegment.silent(duration=20000) 
        start_time = 0
        # print(chromosome[0],chromosome[1],chromosome[49])
        for sound_name, interval, volume_db in chromosome:
            start_time += interval
            sound_clip = self.tabla_sounds[sound_name]
            sound_clip = sound_clip + volume_db
            audio = audio.overlay(sound_clip, position=int(start_time))
        return audio
