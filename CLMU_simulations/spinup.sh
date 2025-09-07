#!/bin/bash --login
#SBATCH -p multicore
#SBATCH -t 7-0  # Time limit (D-HH:MM), max 4 days
#SBATCH -n 2    # Number of cores, max 12 for 1 GPU V100
#SBATCH --job-name  spinup
#SBATCH --output  spinup.out
#Junjie Yu, 2025-03-13

source activate pyclmuapp

#python pull.py # must pull the image first
python 1_spinup.py --container_type singularity 