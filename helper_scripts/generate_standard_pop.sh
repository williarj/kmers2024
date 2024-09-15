# Run a full test that generates a population with the following variables and calculates the diversity of the sampled individuals
# Written by Olivia Davis

OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Model Variables (Defaults)
ref_seq="./arabidopsis_data/high_repeat_region.txt"
mut_rate=0.00001
coverage=10
num_indv=10
seed=101
km=10
cpus=1
generations=1000
pop_size=100
pop=0
test_name="P$pop"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--cov) coverage="$2"; shift ;;
        -k|--kmer) km="$2"; shift ;;
        -m|--mut) mut_rate="$2"; shift ;;
        -n|--name) test_name="$2"; shift ;;
        -i|--indvs) num_indv="$2"; shift ;;
        -d|--id) id="$2"; shift ;;
        -p|--size) pop_size="$2"; shift ;;
        -cp|--cpus) cpus="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "coverage: $coverage and kmer: $km and mut: $mut_rate and cpus: $cpus"

# File / Naming Variables
tree_file_name=$test_name".trees"
tree_path="./SLIM/generated_trees/sim_$id/"$tree_file_name
output_file="./output/"$test_name".csv"
standard_folder="./standard_test/sim_$id"

# Helper Variables (don't change)
reads=$(echo $((coverage*100000/126)))
fasta_file_name=$test_name".fa"
fasta_file_path="$standard_folder/fasta_files/"$fasta_file_name
output_pop_folder="./arabidopsis_sim_data/sim_$id"
output_pop_file_path="$output_pop_folder/sim_"$id"_genomes.fa"
csv_path="./arabidopsis_sim_data/sim_$id/sim_info_$id.csv"
csv_header="id,pop,pop_size,generations,sampled individuals,mutation rate,coverage,k-length,average pi"
csv_line_one="$id,$pop,$pop_size,$generations,$num_indv,$mut_rate,$coverage,$km,"
split_fasta_path="$standard_folder/fasta_files/"$test_name"/"
read_file_path="$output_pop_folder/reads/"$test_name"/"

# [Commands Run]

# Simulate population with SLIM. Add mutations and sample n individuals from population to create multi fasta file. (where n = num_indv)

mkdir $standard_folder
mkdir $standard_folder/fasta_files/

mkdir ./SLIM/generated_trees/sim_$id

./SLIM/slimexe -d "file_name='./SLIM/generated_trees/sim_$id/$tree_file_name'" -d mut_rate=$mut_rate -d pop_size=$pop_size ./SLIM/generate_tree.slim &&

mkdir $output_pop_folder &&

echo "$csv_header" > $csv_path &&

python3 ./tskit_msprime/stand_tree_to_fasta.py $tree_path $fasta_file_path $seed $num_indv $ref_seq $csv_path $csv_line_one&&

python3 ./helper_scripts/format_pop_fasta.py $fasta_file_path $num_indv $pop $id $output_pop_file_path && 

mkdir $split_fasta_path &&

python3 ./tskit_msprime/splitfasta.py $fasta_file_path $split_fasta_path &&

rm -r $standard_folder/ &&
rm -r ./SLIM/generated_trees/*