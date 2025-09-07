#!/bin/bash --login
#SBATCH -p multicore   # Partition name is required
#SBATCH -t 4-0  # Time limit (D-HH:MM), max 4 days
#SBATCH -n 2    # Number of cores, max 12 for 1 GPU V100
#SBATCH --job-name  getlsh
#SBATCH --output  get_lsh.out

#Junjie Yu, 2025-03-20

source activate pyclmuapp

python 0_get_lhs.py --n 100000