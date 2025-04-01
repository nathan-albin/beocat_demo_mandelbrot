# Beocat Demo - The Mandelbrot Set
## Introduction
This is a very simple example that shows how to use Beocat resources to visualize a portion of the Mandelbrot set.

## Setup
After cloning the repository, you'll need to set up a Python environment to work with. The job scripts assume that your environment is located in `/fastscratch/$USER/mandelbrot_env`. To set up the environment, you'll need to make sure you have created a subdirectory for yourself in `/fastscratch`. If you haven't, use the command
```bash
mkdir /fastscratch/$USER
```
Next, you'll need to load the Python and CUDA modules. Do this with the command
```bash
module load Python/3.10.4 CUDA
```
To create the Python environment, make sure you're in the demo code directory and then enter the following commands.
```bash
python -m venv /fastscratch/$USER/mandelbrot_env
. /fastscratch/$USER/mandelbrot_env/bin/activate
pip install -r requirements.txt
```
This creates the Python virtual environment, activates it, and installs the required software libraries into it.

> [!IMPORTANT]
> The `/fastscratch` filesystem is intended for temporary files. Once you're finished with the code, you should delete your virtual environment.
> ```bash
> rm -rf /fastscratch/$USER/mandelbrot_env/
> ```

## Running the code
Once you've set up the virtual environments, you can run the examples.

To compute the Mandelbrot image on a single processor, run
```bash
sbatch run1.sh
```

To compute the same image in parallel using multi-threading on 16 cores, run
```bash
sbatch run16.sh
```

To compute the image using CUDA on a GPU, run
```bash
sbatch run_cuda.sh
```

These commands will generate the image files `mandelbrot_3000x3000_1P.png`, mandelbrot_3000x3000_16P.png` and `mandelbrot_3000x3000_cuda.png` respectively. It will also generate one SLURM output file per job. To view the outputs (e.g., to compare runtimes), you can run
```bash
cat *.out
```
