#!/bin/bash

## request 16 CPUs
#SBATCH --nodes=1 --cpus-per-task=16

## load python
module load Python/3.10.4-GCCcore-11.3.0

## change to program directory
cd $HOME/beocat_demo_mandelbrot

## load our virtual environment
. /fastscratch/$USER/mandelbrot_env/bin/activate

## run the Python script
python mandelbrot.py --width 3000 --height 3000 --proc 16
