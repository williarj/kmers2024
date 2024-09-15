# K-mer Diversity Metrics Pipeline


## Requirements and Versions

KMC 3.2.2
* Make sure the KMC executable and bin files are in the 'KMC3' folder.
* Easiest way to do this is run the command `tar -xvzf KMC3/KMC3.2.2.linux.x64.tar.gz`
    * The compressed KMC3 file can be replaced with a different KMC release as long as everything is extracted in the KMC3 folder.
    * If you would like to manually change where the KMC3 executable is called from, modify `./helper_scripts/count_kmers.sh`

Python 3.8.16

### Python Packages
* Note: Installing pysam requires a linux or MacOS system and is necessary for running the scripts

<div style="margin-left: auto;
            margin-right: auto;
            width: 30%">

|Package         |Version|
|----------------|-------|
|InSilicoSeq     |1.3.5  |
|Biopython       |1.84   |
|SciPy           |1.13.1 |
|joblib          |1.4.2  |
|mmh3            |4.1.0  |
|msprime         |1.0.2  |
|tskit           |0.5.6  |
|pyslim          |1.0.4  |
|scikit-learn    |1.5.2  |
|gsl             |2.6    |
|InSilicoSeq     |2.0.1  |
|biopython       |1.83   |

</div>
<center>
(full list in `environment_specs/requirements.txt`)
</center>

### Using Conda

Environments needed:
conda-forge, bioconda, r

To create an environment with the exact specifications files

from exported yml file:

`conda create --name [environment name] --file enviroment_specs/kmer_env.txt`

from specific requirements:

`conda create --name [environment name] --file enviroment_specs/requirements.txt`

## How to Use

For any of these processes make sure to set the simulation variables (mutation, coverage, k-length, individuals, simulation ids, etc) in
helper_scripts/simulation.py

A new simulation class can be made if you want multiple as long as the import is changed in each of the python files (`generate_standard_pop`, `generate_coverage`, `count_kmers`, `calculate_scores`)

### Running the full pipeline

`bash run_full_pipeline.sh`

### Running only population simulation

`python ./helper_scripts/generate_standard_pop.py`

### Running only coverage generation

`python ./helper_scripts/generate_standard_pop.py`

### Running only k-mer counting

`python ./helper_scripts/count_kmers.py`

### Running only diversity score calculation

`python ./helper_scripts/calculate_scores.py`

* If modifications need to be made to what calculations are done, or with what parameters, please scroll down to the "MODIFY HERE" comment in `diversity_metrics/measure_diversity.py`

### Viewing/Visualizing data

A data for one particular simulation will be in the folder of that simulation in two csv files.
The first file, `sim_info_[id].csv`, keeps track of the id and parameters of the simulation.
The second file, `sim_[id]_results...`, stores the data on any diversity score calculations and parameters (if applicable).

See examples in `./plots`