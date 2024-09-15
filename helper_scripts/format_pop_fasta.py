import sys
import re

input_fasta = sys.argv[1]
indvs = sys.argv[2]
pop = sys.argv[3]
id = sys.argv[4]
output = sys.argv[5]

print("\n CONVERTING... \n")

with open(input_fasta) as file:
    data = file.read()

data = re.sub(r'>n[0-9]+',"name",str(data))

for i in range(0,int(indvs)*2):
    new = ">ID" + id + "_" + "P" + pop + "_I" + str(int(i/2)) + "_H" + str(i%2)
    # print(new)
    data = data.replace("name",new,1)

file.close()

outfile = open(output,'w')
outfile.write(data)
outfile.close()