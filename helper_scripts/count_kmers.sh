# Count the k-mers of given samples

OPTIND=1         # Reset in case getopts has been used previously in the shell.

# Initialize our own variables:
# Model Variables
mut_rate=0.00001
coverage=10
num_indv=10
seed=101
div_metric="BC"
km=10
cpus=3
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
output_pop_folder="."
kmer_output=$output_pop_folder/kmer_counts_"x$coverage"_k$km
read_file_path="$output_pop_folder/reads_x$coverage/"$test_name"/"

# [Commands Run]

# Get kmer counts with KMC3

mkdir $kmer_output/ &&
mkdir $kmer_output/tmp/ &&
mkdir $kmer_output/tmp/$test_name"/" &&
mkdir $kmer_output/$test_name"/" &&

for i in $(seq 0 $((2*num_indv-1)))
do
    ../../KMC3/bin/kmc -t$cpus -k$km -ci$min_count $read_file_path"n"$i"_R1.fastq" $kmer_output/tmp/$test_name"/n"$i"_R1" .&&

    ../../KMC3/bin/kmc -t$cpus -k$km -ci$min_count $read_file_path"n"$i"_R2.fastq" $kmer_output/tmp/$test_name"/n"$i"_R2" . &&

    ../../KMC3/bin/kmc_tools -t$cpus simple $kmer_output/tmp/$test_name"/n"$i"_R1" $kmer_output/tmp/$test_name"/n"$i"_R2" union $kmer_output/tmp/$test_name/n$i &&

    ../../KMC3/bin/kmc_tools -t$cpus transform $kmer_output/tmp/$test_name/n$i  dump $kmer_output/$test_name/n$i.txt
done

for i in $(seq 0 $((2*num_indv-1)))
do
    for j in $(seq 0 $((2*num_indv-1)))
    do
        if [ $i -lt $j ]
        then
            ../../KMC3/bin/kmc_tools -t$cpus simple $kmer_output/tmp/$test_name"/n"$i $kmer_output/tmp/$test_name"/n"$j intersect $kmer_output/tmp/$test_name/n$i"_n"$j &&

            ../../KMC3/bin/kmc_tools -t$cpus transform $kmer_output/tmp/$test_name/n$i"_n"$j  dump $kmer_output/$test_name/n$i"_inter_n$j".txt
        fi
    done
done