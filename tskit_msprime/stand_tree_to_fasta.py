import tskit
import pyslim
import numpy as np
import sys

# Get user input
# inputfile - path to the SLIM tree file
# outputfile - path where the fasta file will be saved
# rand_seed - seed t use for numpy's random number generation
# ref_seq - reference sequence that we add mutations to

inputfile = sys.argv[1]
outputfile = sys.argv[2]
rand_seed = int(sys.argv[3]) #Seed
num_indv = int(sys.argv[4])
ref_seq = sys.argv[5]
csv_output = sys.argv[6]
csv_line = sys.argv[7]

with open(ref_seq) as file:
    data = file.read().replace('\n','')

rng = np.random.default_rng(seed=rand_seed)
slim_ts = tskit.load(inputfile)

alive_inds = pyslim.individuals_alive_at(slim_ts, 0)
keep_indivs = rng.choice(alive_inds, num_indv, replace=False)
keep_nodes = []
for i in keep_indivs:
  keep_nodes.extend(slim_ts.individual(i).nodes)

sts = slim_ts.simplify(keep_nodes, keep_input_roots=True)

nts = pyslim.generate_nucleotides(ts=sts,reference_sequence=data)
nts = pyslim.convert_alleles(nts)

print("Num individuals:")
print(nts.num_individuals)

nts.write_fasta(outputfile)

print(f"The tree sequence now has {nts.num_mutations} mutations,\n"
      f"and mean pairwise nucleotide diversity is {nts.diversity():0.5e}.")

f = open(csv_output,"a")
f.write(csv_line+str(nts.diversity()))
f.close()

file.close()