import chevron
import datetime


def create_slurm_header(args):
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
    data = {"job_name": args.job_name,
            "nodes": args.nodes,
            "ntasks": args.ntasks,
            "mem": args.mem,
            "time": args.time}

    if args.gpus is not None:
        slurm_template += "#SBATCH --gpus={{gpus}}\n"
        data.update({"gpus": args.gpus})

    if args.kwargs:
        kwarg_dict = {k:v for k,v in [b.split("=") for b in args.kwargs.split(",")]}
        for k in kwarg_dict.keys():
            if "_" in k:
                k = k.replace("_", "-")
            slurm_template += f"#SBATCH --{k}=" + "{{" + k + "}}\n"
        data.update(kwarg_dict)

    slurm_header = chevron.render(slurm_template, data=data)

    if args.file_name is not None:
        with open(args.file_name, "w") as f:
            f.write(slurm_header)

    return slurm_header
def create_slurm_header_old(file_name=f"sbatch_{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}.sh",
                        job_name=f"slurm_job_{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}",
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
    data = {"job_name": args.job_name,
            "nodes": args.nodes,
            "ntasks": args.ntasks,
            "mem": args.mem,
            "time": args.time}

    if args.gpus is not None:
        slurm_template += "#SBATCH --gpus={{gpus}}\n"
        data.update({"gpus": args.gpus})

    if kwargs:
        for k in kwargs.keys():
            if "_" in k:
                k = k.replace("_", "-")
            slurm_template += f"#SBATCH --{k}=" + "{{" + k + "}}\n"
        data.update(kwargs)

    slurm_header = chevron.render(slurm_template, data=data)

    if args.file_name is not None:
        with open(args.file_name, "w") as f:
            f.write(slurm_header)

    return slurm_header