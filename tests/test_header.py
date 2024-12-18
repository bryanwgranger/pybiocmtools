import chevron
import datetime
import os
import re

def create_slurm_header(job_name=f"slurm_job_{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}",
                        nodes=1,
                        ntasks=8,
                        mem="32gb",
                        time="48:00:00",
                        gpus=None,
                        **kwargs):

    slurm_template = ("#!/bin/bash\n"
                      "#SBATCH --job-name={{job_name}}\n"
                      "#SBATCH --nodes={{nodes}}\n"
                      "#SBATCH --ntasks-per-node={{ntasks}}\n"
                      "#SBATCH --mem={{mem}}\n"
                      "#SBATCH --time={{time}}\n"
                      "#SBATCH --output=slurm-%j.out\n"
                      "#SBATCH --error=slurm-%j.err\n"
                      "#SBATCH -p musc3\n"
                      )
    data = {"job_name": job_name,
            "nodes": nodes,
            "ntasks": ntasks,
            "mem": mem,
            "time": time}

    if gpus:
        slurm_template += "#SBATCH --gpus={{gpus}}\n"
        data.update({"gpus": gpus})

    if kwargs:
        for k in kwargs.keys():
            slurm_template += f"#SBATCH --{k}=" + "{{" + k + "}}\n"
        data.update(kwargs)

    slurm_header = chevron.render(slurm_template, data=data)

    return slurm_header

# print(create_slurm_header(job_name="test_job",
#                           gpus=2,
#                           mail_type="FAIL",
#                           bryan="granger"))

def create_cellranger_script(fastq_path,
                             outs_path,
                             transcriptome_path,
                             script_prefix=None):
    #fastq_files = os.listdir(fastq_path)

    if not os.path.exists(outs_path):
        os.makedirs(outs_path)

    cr_file_template = ("mkdir -p {{outs_path}}\n"
                        "cd {{outs_path}}\n\n"
                        "singularity exec -B /project/stefanoberto/musc:/project/stefanoberto/musc \\\n"
                        "\t--pwd {{outs_path}} \\\n"
                        "\t/project/stefanoberto/musc/singularity_images/biocm-cellranger_latest.sif \\\n"
                        "\tcellranger count \\\n"
                        "\t--id={{sample}} \\\n"
                        "\t--sample={{sample}} \\\n"
                        "\t--transcriptome={{transcriptome_path}} \\\n"
                        "\t--fastqs={{fastq_path}} \\\n"
                        "\t--localcores=24 \\\n"
                        "\t--localmem=200")
    fq_extension = 'fq$|fq\.gz$|fastq$|fastq\.gz$'
    fastq_files = [f for f in os.listdir(fastq_path) if re.search(string=f, pattern=fq_extension)]
    samples = set([re.split(pattern="_S\d_", string=s)[0] for s in fastq_files])
    for sample in samples:
        script_name = f"{script_prefix}_{sample}.sh" if script_prefix else f"cr_{sample}.sh"
        with open(script_name, "w") as outfile:
            outfile.write(create_slurm_header(job_name=script_name.replace('.sh', ''),
                                              nodes=1,
                                              ntasks=32,
                                              mem="250gb",
                                              time="72:00:00",
                                              gpus=None,))

            outfile.write("\n")
            outfile.write(chevron.render(template=cr_file_template,
                                         data={"sample": sample,
                                               "transcriptome_path": transcriptome_path,
                                               "fastq_path": fastq_path,
                                               "outs_path": outs_path,}))

test_path = "/Users/bryanwgranger/biocm/projects/berto"

create_cellranger_script(fastq_path=test_path,
                         outs_path="/Users/bryanwgranger/biocm/projects/berto/script_test",
                         transcriptome_path="/project/stefanoberto/musc/reference/HUMAN/RNA/hg38_full",)