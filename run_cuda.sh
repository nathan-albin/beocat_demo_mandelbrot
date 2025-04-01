#!/bin/bash

## request a GPU
#SBATCH --gres=gpu:1

## load python
module load Python/3.10.4-GCCcore-11.3.0
module load CUDA

## changeOA to program directory
cd $HOME/beocat_demo_mandelbrot

## load our virtual environment
. /fastscratch/$USER/mandelbrot_env/bin/activate

## run the Python script
python mandelbrot_cuda.py --width 3000 --height 3000
