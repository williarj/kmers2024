import msprime
import tskit
import pyslim
import numpy as np
import sys

# Get user input
# inputfile - path to the SLIM tree file
# outputfile - path where the fasta file will be saved
# rand_seed - seed t use for numpy's random number generation

inputfile = sys.argv[1]
outputfile = sys.argv[2]
rand_seed = int(sys.argv[3]) #Seed
num_indv = int(sys.argv[4])

rng = np.random.default_rng(seed=rand_seed)
slim_ts = tskit.load(inputfile)

alive_inds = pyslim.individuals_alive_at(slim_ts, 0)
keep_indivs = rng.choice(alive_inds, num_indv, replace=False)
keep_nodes = []
for i in keep_indivs:
  keep_nodes.extend(slim_ts.individual(i).nodes)

sts = slim_ts.simplify(keep_nodes, keep_input_roots=True)

nts = pyslim.generate_nucleotides(sts)
nts = pyslim.convert_alleles(nts)

print("Num individuals:")
print(nts.num_individuals)

# print("Num nodes:")
# print(nts.num_trees)

# Convert tree to FASTA format

nts.write_fasta(outputfile)

print(f"The tree sequence now has {nts.num_mutations} mutations,\n"
      f"and mean pairwise nucleotide diversity is {nts.diversity():0.3e}.")


# count = 0

# for node in nts.trees():
#   print("Tree #" + str(count))
#   print(node.num_individuals)
#   if(node.num_edges == 0):
#     node.write_fasta("./fasta_files/high_mut_fasta%d.fa" % count/2)
#   count += 1