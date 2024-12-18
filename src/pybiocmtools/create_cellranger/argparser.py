import argparse


def add_subparser_args(subparsers: argparse) -> argparse:

    subparser = subparsers.add_parser("create-cellranger",
                                      description="Create a Cellranger job script",
                                      help="Create a Cellranger job script",
                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    subparser.add_argument('--fastq-path', default=None, required=True, dest="fastq_path",)
    subparser.add_argument('--transcriptome-path', default=None, required=True, dest="transcriptome_path",)
    subparser.add_argument('--outs-path', default='./run', required=False, dest="outs_path",)
    subparser.add_argument('--script-prefix', default=None, required=False, dest="script_prefix",)
    subparser.add_argument('--singularity', default=False, action="store_true", required=False, dest="singularity",)

    return subparsers