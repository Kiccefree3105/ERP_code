#!/bin/bash --login
#SBATCH -p multicore   # Partition name is required
#SBATCH -t 4-0  # Time limit (D-HH:MM), max 4 days
#SBATCH -n 32    # Number of cores, max 12 for 1 GPU V100
#SBATCH --job-name  lshexp
#SBATCH --output  lshexp.out
#Junjie Yu, 2025-03-20

source activate pyclmuapp
echo "Start time: $(date)"
python 2_lhs_exp.py --container_type singularity --input_file lhs_exps_dict.pkl --nproc 32
tar -czvf lhs_exp.tar.gz ./lhs_data/
mv ./lhs_data/ ./lhs_data_exp/
echo "End time: $(date)"

echo "Start time: $(date)"
python 2_lhs_exp.py --container_type singularity --input_file features_Manchester.pkl --nproc 32
tar -czvf man_exp.tar.gz ./lhs_data/
mv ./lhs_data/ ./man_data/
echo "End time: $(date)"