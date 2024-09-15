# This program generates k-mers of the simulations starting from the start_id (inclusive) to the end_id (exclusive)

import os
import multiprocessing
from joblib import Parallel, delayed
from simulation import Simulation as Sim

procs = Sim.procs
test_path = Sim.test_path
coverages = Sim.coverages
kmers = Sim.kmers
start_id = Sim.start_id
end_id = Sim.end_id

def count_kmers(id):
    for kmer in kmers:
        for cov in coverages:
            sim_exists = os.path.isdir(test_path + "sim_" + str(id) + "/kmer_counts_x" + str(cov) + "_k" + str(kmer))
            if(sim_exists == False):
                os.chdir('./arabidopsis_sim_data/sim_'+str(id))
                print("generating k: %d, id: %i, c: %d,"%(kmer,id,cov))
                os.system('bash ../../helper_scripts/count_kmers.sh -k %d -d %d -c %d' %(kmer,id,cov))
                os.chdir('../../')

processed_list = Parallel(n_jobs=procs)(delayed(count_kmers)(i) for i in range(start_id,end_id))
count_kmers(start_id)