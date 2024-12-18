import argparse
import datetime
import os


def add_subparser_args(subparsers: argparse) -> argparse:
    subparser = subparsers.add_parser("create-sbatch",
                                      description="Create a SBATCH job script",
                                      help="Create a SBATCH job script",
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser.add_argument("--file-name", default=f"sbatch_{datetime.datetime.now().strftime('%Y-%m-%dT%H_%M')}.sh",
                           dest="file_name",
                           help="Name of SBATCH script to create")
    subparser.add_argument("--job-name", default=f"slurm_job_{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M')}",
                           dest="job_name",
                           type=str,
                           help="Name of SBATCH job")

    subparser.add_argument("--nodes", default=1, type=int)
    subparser.add_argument("--ntasks", default=8, type=int)
    subparser.add_argument("--mem", default="32gb", type=str)
    subparser.add_argument("--time", default="48:00:00", type=str)
    subparser.add_argument("--gpus", default=None)
    subparser.add_argument("--kwargs", default=None, type=str,
                           help="Additional arguments to pass to sbatch script generator. "
                                "Pass them in the format: KEY=VALUE,KEY2=VALUE2")

    return subparsers