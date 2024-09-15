# There is where to define the variables of the simulation so it can be importanted into the separate python files

# Variable:
# procs = number of processors to use in parallel
# test_path -> the directory where the simulation fasta files and other data are held
# individuals -> number of individuals, or samples, in each population
# kmers -> a list of the length k of k-mers we want to generate
# remove_k -> the mininum number of k-mers counted, the rest are deleted
# coverages -> a list of coverages to simulate when simulating reads
# mutations -> a list of mutations to simulate when generating a population

class Simulation:
    procs = 1

    start_id = 2 # Inclusive
    end_id = 3 # Exclusive

    test_path = "./arabidopsis_sim_data/"

    mutations = [0.000001,0.00001,0.00003,0.00005,0.0001,0.0002]
    individuals = 10

    coverages = [10]

    kmers=[10]
    remove_k = 5