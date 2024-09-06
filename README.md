# Tabla Composition Evolutionary Algorithms

This repository contains the research project completed for the course CS-451: Computational Intelligence at Habib University, Karachi. The main code is housed in the `EA` folder and is designed to evolve tabla compositions using evolutionary algorithms.

## Dependencies

* Python
* Numpy

## Problem Introduction

### Tabla Composition Generation

This project focuses on generating tabla compositions using evolutionary algorithms. Tabla is a popular percussion instrument in South Asian music, and composing tabla sequences involves arranging different rhythmic patterns called "bols."

## Algorithm

The algorithm follows these steps:
* Generate a random population of _population_size_ and assign them fitness values.
* Select parents using a _parent_selection_scheme_.
* Generate offsprings from parents using a crossover method.
* Mutate these offsprings based on the _mutation_rate_ probability.
* Calculate the fitness of new offsprings.
* Select members for the next generation through a _survivor_selection_scheme_.
* Repeat the steps until the end of _generations_no_.

The _italicized_ terms are configurable by the user during runtime.

## Usage

Navigate to the base folder and run the main script with the required parameters:

```sh
python EA/main.py p1 p2 ... p8
```

For a complete list of parameters and their values, refer to [Parameters](#parameters).

### Example

```sh
python EA/main.py ts_4 tr 30 10 50 0.5 10 16
```

## Parameters

1. **Parent Selection Scheme**: Specify a selection scheme for choosing parents to generate offsprings.
2. **Survival Selection Scheme**: Specify a selection scheme to decide which chromosomes will survive to the next generation.
3. **Population Size**: Initial population size.
4. **Offspring Size**: Number of offsprings to be generated in each generation.
5. **Generations Number**: Number of generations the algorithm will run, which is also the termination criterion.
6. **Mutation Rate**: The probability that each offspring will undergo mutation.
7. **Iterations**: Number of iterations of the entire process to generate multiple samples for averaging.
8. **Length of Tabla Composition**: Length of the tabla composition to be evolved.

## Auxiliary Files

* **graph.py**: Used to create graphs from the output data.
* **main_csv.py**: Used to generate datasets for analysis.

## Data

The `Bols` folder contains all the input data of bols used for generating tabla compositions.

## Selection Schemes

The following selection schemes are implemented and can be specified using their abbreviations:

* **Random**: rn
* **Tournament**: ts_*size*, where *size* specifies the size of the tournament.
* **Rank Based Selection**: rbs
* **Fitness Proportion Selection**: fps
* **Truncation**: tr

## Authors

* [Azeem Haider](https://github.com/A-Haider13)
* [Ali Siddiqui](https://github.com/AliSid10)
* [Mustafa Sohail](https://github.com/Mustafasohail7)

## License

[MIT](https://choosealicense.com/licenses/mit/)
