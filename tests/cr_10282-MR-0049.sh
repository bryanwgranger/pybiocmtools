#!/bin/bash
#SBATCH --job-name=cr_10282-MR-0049
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mem=250gb
#SBATCH --time=72:00:00
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err
#SBATCH -p musc3

mkdir -p /Users/bryanwgranger/biocm/projects/berto/script_test
cd /Users/bryanwgranger/biocm/projects/berto/script_test

singularity exec -B /project/stefanoberto/musc:/project/stefanoberto/musc \
	--pwd /Users/bryanwgranger/biocm/projects/berto/script_test \
	/project/stefanoberto/musc/singularity_images/biocm-cellranger_latest.sif \
	cellranger count \
	--id=10282-MR-0049 \
	--sample=10282-MR-0049 \
	--transcriptome=/project/stefanoberto/musc/reference/HUMAN/RNA/hg38_full \
	--fastqs=/Users/bryanwgranger/biocm/projects/berto \
	--localcores=24 \
	--localmem=200