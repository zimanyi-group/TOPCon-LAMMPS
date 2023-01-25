#!/bin/bash -l
#! -cwd
#! -j y
#! -S /bin/bash
#SBATCH -D ./
#SBATCH --job-name=TOPCon
#SBATCH --partition=med2 # Partition you are running on. Options: low2, med2, high2
#SBATCH --output=/home/amdiggs/projects/LAMMPS-out/TOPCon-%j.txt
#SBATCH --mail-user="amdiggs@ucdavis.edu"
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL

#======memory for neb I will specifically set up a grid nxm makes n-replicas that use m sub-tasks ntasks = n*m
#SBATCH --ntasks=512
#SBATCH --ntasks-per-node=256 
#SBATCH --cpus-per-task=1 
#SBATCH --mem=64G
#SBATCH -t 2-12:00
#SBATCH --array=0-1

NSI=(319 370)
NOX=(638 540)

# Here we will run a hybrid MPI/OPENMP code. E.g. we have multiple tasks, and each task has multiple threads
export OMP_NUM_THREADS=1
j=$SLURM_JOB_ID
i=$SLURM_ARRAY_TASK_ID

srun $HOME/lmp_mpi -var nsi ${NSI[i]} -var nox ${NOX[i]} -var rand $RANDOM -log siox-${i}.log -in cSi-SiOx.in
