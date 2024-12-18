import os
import re
import chevron
#from pybiocmtools.create_sbatch.create_sbatch import create_slurm_header
from pybiocmtools.slurm_tools import create_slurm_header
def create_cellranger_script(args):

    if not os.path.exists(args.outs_path):
        os.makedirs(args.outs_path)

    cr_file_template = ("mkdir -p {{outs_path}}\n"
                        "cd {{outs_path}}\n\n"
                        "\tcellranger count \\\n"
                        "\t--id={{sample}} \\\n"
                        "\t--sample={{sample}} \\\n"
                        "\t--transcriptome={{transcriptome_path}} \\\n"
                        "\t--fastqs={{fastq_path}} \\\n"
                        "\t--localcores=24 \\\n"
                        "\t--localmem=200")

    cr_file_template_singularity = ("mkdir -p {{outs_path}}\n"
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
    fastq_files = [f for f in os.listdir(args.fastq_path) if re.search(string=f, pattern=fq_extension)]
    samples = set([re.split(pattern="_S\d_", string=s)[0] for s in fastq_files])
    for sample in samples:
        script_name = f"{args.script_prefix}_{sample}.sh" if args.script_prefix else f"cr_{sample}.sh"
        file_out_path = os.path.join(args.outs_path, script_name)
        with open(file_out_path, "w") as outfile:
            outfile.write(create_slurm_header(job_name=script_name.replace('.sh', ''),
                                              nodes=1,
                                              ntasks=32,
                                              mem="250gb",
                                              time="72:00:00",
                                              gpus=None,))

            outfile.write("\n")
            if args.singularity:
                outfile.write(chevron.render(template=cr_file_template_singularity,
                                             data={"sample": sample,
                                                   "transcriptome_path": args.transcriptome_path,
                                                   "fastq_path": args.fastq_path,
                                                   "outs_path": args.outs_path,}))
            else:
                outfile.write(chevron.render(template=cr_file_template,
                                             data={"sample": sample,
                                                   "transcriptome_path": args.transcriptome_path,
                                                   "fastq_path": args.fastq_path,
                                                   "outs_path": args.outs_path, }))
#
# if __name__ == "__main__":
#     # setting the parameters
#     import argparse
#
#     parser = argparse.ArgumentParser(description='Create Anndata file from prepared Seurat directory',
#                                      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument('--fastq_path', default=None, required=True)
#     parser.add_argument('--transcriptome_path', default=None, required=True)
#     parser.add_argument('--outs_path', default='./run', required=False)
#     parser.add_argument('--script_prefix', default=None, required=False)
#
#     args = parser.parse_args()
#
#     create_cellranger_script(args)