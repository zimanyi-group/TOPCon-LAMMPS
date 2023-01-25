#!/bin/bash -l
#! -cwd
#! -j y
#! -S /bin/bash
#SBATCH -D ./
#SBATCH --job-name=Therm
#SBATCH --partition=med2 # Partition you are running on. Options: low2, med2, high2
#SBATCH --output=/home/amdiggs/projects/LAMMPS-out/Therm-%j.txt
#SBATCH --mail-user="amdiggs@ucdavis.edu"
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

#======memory for neb I will specifically set up a grid nxm makes n-replicas that use m sub-tasks ntasks = n*m
#SBATCH --ntasks=512
#SBATCH --ntasks-per-node=256 
#SBATCH --cpus-per-task=1 
#SBATCH --mem=64G
#SBATCH -t 2-12:00
# SBATCH --array=0-1

RAT=(1.14 1.54)
# Here we will run a hybrid MPI/OPENMP code. E.g. we have multiple tasks, and each task has multiple threads
export OMP_NUM_THREADS=1
j=$SLURM_JOB_ID
i=$SLURM_ARRAY_TASK_ID
DATFILE=$HOME/projects/TOPCon/SiOx/NUC2/DATA-FILES/siox-${RAT[1]}.dat
srun $HOME/lmp_mpi -var datfile $DATFILE -var ratio ${RAT[1]} -log siox-${RAT[1]}.log -in therm.in
