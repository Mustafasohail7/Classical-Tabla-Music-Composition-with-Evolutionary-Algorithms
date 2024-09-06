import sys
from EA import EA

def main():
    parent_selection = selection_scheme(sys.argv[1])
    survivor_selection = selection_scheme(sys.argv[2])
    pop_size = int(sys.argv[3])
    offspring_size = int(sys.argv[4])
    generations_no = int(sys.argv[5])
    mutation_rate = float(sys.argv[6])
    iterations = int(sys.argv[7])
    length = 150
    good_pairs = [("DHIN","TA"),("TIN","TA")]
    EA(pop_size, offspring_size, generations_no, mutation_rate, iterations, parent_selection, survivor_selection, length, good_pairs).run()

def selection_scheme(scheme):
    if scheme=="fps":
        return "fitness_prop_selection"
    elif scheme=="rbs":
        return "rank_based_selection"
    elif scheme=="tr":
        return "truncation"
    elif scheme=="rn":
        return "random"

if __name__ == "__main__":
    main()