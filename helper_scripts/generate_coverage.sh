# Run a full test that generates a population with the following variables and calculates the diversity of the sampled individuals
# Written by Olivia Davis

OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
# Model Variables
mut_rate=0.00001
coverage=10
num_indv=10
seed=101
div_metric="BC"
km=10
cpus=1
min_count=0
pop=0
generations=1000
pop_size=100
id=0000
test_name="P$pop"
type="BC"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--cov) coverage="$2"; shift ;;
        -k|--kmer) km="$2"; shift ;;
        -m|--mut) mut_rate="$2"; shift ;;
        -n|--name) test_name="$2"; shift ;;
        -t|--type) type="$2"; shift ;;
        -i|--indvs) num_indv="$2"; shift ;;
        -d|--id) id="$2"; shift ;;
        -p|--size) pop_size="$2"; shift ;;
        -cp|--cpus) cpus="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

echo "coverage: $coverage and kmer: $km and mut: $mut_rate and cpus: $cpus"

# Helper Variables (don't change)
reads=$(echo $((coverage*100000/126)))
output_pop_folder="./arabidopsis_sim_data/sim_$id"
output_pop_file_path="$output_pop_folder/sim_"$id"_genomes.fa"
kmer_output=$output_pop_folder/kmer_counts_"x$coverage"_k$km
read_file_path="$output_pop_folder/reads_x$coverage/"$test_name"/"
split_fasta_path="$output_pop_folder/split_fastas/"

# [Commands Run]

# Generate new coverage

mkdir -p $split_fasta_path&&
mkdir -p "$output_pop_folder/reads_x$coverage/"&&
mkdir -p $read_file_path &&

python ./helper_scripts/unformat_pop_fasta.py $output_pop_file_path $split_fasta_path&&

for i in $(seq 0 $((2*num_indv-1)))
do
    iss generate --genomes $split_fasta_path"n"$i".fa" --cpus $cpus --n_reads $reads --model hiseq --output $read_file_path"/n"$i
done
