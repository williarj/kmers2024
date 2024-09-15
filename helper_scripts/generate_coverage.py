import os
import multiprocessing
from joblib import Parallel, delayed
from simulation import Simulation as Sim

procs = Sim.procs
test_path = Sim.test_path
coverages = Sim.coverages
start_id = Sim.start_id
end_id = Sim.end_id

def gen_coverage(id):
    for cov in coverages:
        sim_exists = os.path.isdir(test_path + "sim_" + str(id))
        if(sim_exists):
            print("./helper_scripts/generate_coverage.sh -d %d -c %d"%(id,cov))
            os.system("bash ./helper_scripts/generate_coverage.sh -d %d -c %d"%(id,cov))

processed_list = Parallel(n_jobs=procs)(delayed(gen_coverage)(i) for i in range(start_id,end_id))

gen_coverage(start_id)