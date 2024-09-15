import random as rand
import os
from timeit import default_timer as timer
from joblib import Parallel, delayed
from simulation import Simulation as Sim

rand.seed(404)

procs = Sim.procs
test_path = Sim.test_path
ind = Sim.individuals
muts = Sim.mutations
coverages = Sim.coverages
start_id = Sim.start_id
end_id = Sim.end_id

def create_sim(id):
    mut = muts[id%6]
    sim_exists = os.path.isdir(test_path + "sim_" + str(id))
    if(sim_exists != True):
        print("Making simulation %d...", id)
        os.system('bash ./helper_scripts/generate_standard_pop.sh -i %d -m %f -d %s' %(ind,mut,id))
    id += 1

processed_list = Parallel(n_jobs=procs)(delayed(create_sim)(i) for i in range(start_id,end_id))