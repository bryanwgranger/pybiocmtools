import chevron
import datetime


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

print(create_slurm_header(job_name="test_job",
                          gpus=2,
                          mail_type="FAIL",
                          bryan="granger"))

