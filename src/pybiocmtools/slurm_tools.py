import chevron
import datetime

def create_slurm_header(job_name=f"slurm_job_{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}",
                        nodes=1,
                        ntasks=8,
                        mem="32gb",
                        time="48:00:00"
                        ):
    file = "/Users/bryanwgranger/biocm/biocm-tools/py_tools/slurm.mustache"

    data = {"job_name": job_name,
            "nodes": nodes,
            "ntasks": ntasks,
            "mem": mem,
            "time": time}

    with open(file, "r") as f:
        slurm_header = chevron.render(f, data=data)

    return slurm_header