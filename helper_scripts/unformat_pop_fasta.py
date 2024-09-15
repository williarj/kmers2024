import sys

input_fasta = sys.argv[1]
output = sys.argv[2]
outfile = []

print("\n CONVERTING... \n")

number = 0

for line in open(input_fasta):
    if line.startswith(">"):
        if (outfile != []): 
            outfile.close()
        filename = output + "n" + str(int(number)) +".fa"
        number += 1
        outfile = open(filename,'w')
        outfile.write(line)
    else:
        outfile.write(line)