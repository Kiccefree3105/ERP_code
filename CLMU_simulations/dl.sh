#!/bin/bash --login
#$ -cwd
#$ -pe smp.pe 2

source activate pyclmuapp

pyclmuapp --pyclmuapp_mode get_forcing \
    --lat 53.417 --lon -2.250 --zbot 30 \
    --start_year 2010 --end_year 2023 \
    --start_month 1 --end_month 12 