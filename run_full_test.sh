# Bash script to run the full pipeline

# Simulate a sample population
python ./helper_scripts/generate_standard_pop.py


# Generate reads with the defined set of coverages
python ./helper_scripts/generate_coverage.py

# Count k-mers of given ID and coverage
python ./helper_scripts/count_kmers.py

# Calculate scores
python ./helper_scripts/calculate_scores.py