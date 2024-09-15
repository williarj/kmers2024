import sys
infile = open(sys.argv[1])
outfile = []

output_path = sys.argv[2]

## Note: Splits fasta file outputed by reader

for line in infile:
    if line.startswith(">"):
        genename = line.strip()[1:]
        number = int(genename[1:])
        if (outfile != []): 
            outfile.close()
        genename = line.strip()[1:]
        filename = output_path + "n" + str(int(number)) +".fa"
        outfile = open(filename,'w')
        outfile.write(line)
    else:
        outfile.write(line)
outfile.close()