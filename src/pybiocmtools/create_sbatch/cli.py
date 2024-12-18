from pybiocmtools.base_cli import AbstractCLI
#from src.pybiocmtools.base_cli import AbstractCLI
from .create_sbatch import create_slurm_header

import logging
import os
import sys
import argparse

class CLI(AbstractCLI):
    """CLI implements AbstractCLI from the cellbender package."""

    def __init__(self):
        self.name = 'create-sbatch'
        self.args = None

    def get_name(self) -> str:
        return self.name

    @staticmethod
    def validate_args(args) -> argparse.Namespace:
        """Validate parsed arguments."""

        return args

    @staticmethod
    def run(args):
        """Run the main tool functionality on parsed arguments."""

        # Run the tool.
        return main(args)

def main(args):
    slurm_header = create_slurm_header(args)
    print(f"sbatch script has been created at {args.file_name} with header: \n{slurm_header}")