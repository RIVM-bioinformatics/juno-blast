"""
Juno-blast pipeline
Authors: Alejandra Hernandez-Segura
Organization: Rijksinstituut voor Volksgezondheid en Milieu (RIVM)
Department: Infektieziekteonderzoek, Diagnostiek en Laboratorium
            Surveillance (IDS), Bacteriologie (BPD)     
Date: 17-06-2021   
"""

# Dependencies
import argparse
import base_juno_pipeline
import pathlib
import yaml

class JunoBlastRun():
    """Class with the arguments and specifications that are only for the 
    Juno-blast pipeline but inherit from PipelineStartup and RunSnakemake
    """

    def __init__(self, 
                input_dir, 
                output_dir, 
                evalue=1e-10,
                max_hsps=10,
                culling_limit=10,
                db_dir = "db", 
                cores=8,
                local=True,
                queue='bio',
                unlock=False,
                rerunincomplete=False,
                dryrun=False):
        """Initiating Juno-Blast pipeline"""

        # Pipeline attributes
        self.pipeline_info = {'pipeline_name': "Juno_blast",
                                'pipeline_version': "0.1"}
        self.snakefile = "Snakefile"
        self.sample_sheet = "config/sample_sheet.yaml"
        self.input_dir = pathlib.Path(input_dir)
        self.output_dir = pathlib.Path(output_dir)
        self.db_dir = pathlib.Path(db_dir)
        self.evalue = evalue
        self.max_hsps = int(max_hsps)
        self.culling_limit = int(culling_limit)
        self.workdir = pathlib.Path(__file__).parent.absolute()
        self.useconda = True
        self.usesingularity = False
        self.singularityargs = ""
        self.user_parameters = pathlib.Path('config', 'user_parameters.yaml')
        self.fixed_parameters = pathlib.Path('config', 'user_parameters.yaml')
        self.extra_software_versions = pathlib.Path('config/extra_software_versions.yaml')
        self.output_dir = output_dir
        self.restarttimes = 0       
        # Preparing pipeline to start (generate sample sheet) 
        self.startup = self.start_pipeline()

        # Parse arguments specific from the user
        self.user_params = self.write_userparameters()
        
        # Run snakemake
        snakemake_run = base_juno_pipeline.RunSnakemake(pipeline_name = self.pipeline_info['pipeline_name'],
                                                        pipeline_version = self.pipeline_info['pipeline_version'],
                                                        sample_sheet = self.sample_sheet,
                                                        output_dir = self.output_dir,
                                                        workdir = self.workdir,
                                                        snakefile = self.snakefile,
                                                        cores = cores,
                                                        local = local,
                                                        queue = queue,
                                                        unlock = unlock,
                                                        rerunincomplete = rerunincomplete,
                                                        dryrun = dryrun,
                                                        useconda = self.useconda,
                                                        usesingularity = self.usesingularity,
                                                        singularityargs = self.singularityargs,
                                                        restarttimes = self.restarttimes)

        self.successful_run = snakemake_run.run_snakemake()
        assert self.successful_run, f'Please check the log files'
        
    def start_pipeline(self):
        """Function to start the pipeline (generate sample sheet and save it as a yaml file)"""
        # Taking fasta input as the Startup just to inherit all the same attributes
        # from parent class (PipelineStartup). 
        startup = base_juno_pipeline.PipelineStartup(self.input_dir, input_type = 'fasta')
        # Write sample_sheet
        with open(self.sample_sheet, 'w') as file:
            yaml.dump(startup.sample_dict, file, default_flow_style=False)
        return startup
    
    def write_userparameters(self):

        config_params = {'input_dir': str(self.input_dir),
                        'out': str(self.output_dir),
                        'blast_db': str(self.db_dir),
                        'blast_parameters':{
                            'evalue': self.evalue,
                            'max_hsps': self.max_hsps,
                            'culling_limit': self.culling_limit
                        }
                        }
        
        with open(self.user_parameters, 'w') as file:
            yaml.dump(config_params, file, default_flow_style=False)

        return config_params
        
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = "Juno-blast pipeline. Automated pipeline for blasting fasta files."
    )
    parser.add_argument(
        "-i",
        "--input",
        type = pathlib.Path,
        required = True,
        metavar = "DIR",
        help = "Relative or absolute path to the input directory. It must contain all the assemblies (fasta) files for all samples to be processed (not in subdirectories)."
    )
    parser.add_argument(
        "-o",
        "--output",
        type = pathlib.Path,
        metavar = "DIR",
        default = "output",
        help = "Relative or absolute path to the output directory. If non is given, an 'output' directory will be created in the current directory."
    )
    parser.add_argument(
        "-d",
        "--db_dir",
        type = pathlib.Path,
        required = False,
        metavar = "DIR",
        default = "/mnt/db/juno/blast",
        help = "Relative or absolute path to the directory that contains the databases for all the tools used in this pipeline or where they should be downloaded. Default is: /mnt/db/juno/blast",
    )
    parser.add_argument(
        "-e",
        "--evalue",
        type = float,
        required = False,
        metavar = "NUM",
        default = '1e-10',
        help = "Numeric value used as threshold for the e-value in BLAST. \
            The e-value is the number of expected hits of similar quality \
            (score) that could be found just by chance"
    )
    parser.add_argument(
        "-mh",
        "--max-hsps",
        type = int,
        required = False,
        metavar = "INT",
        default =10,
        help = "Integer value used as threshold for the max_hsps parameter in \
            BLAST. The max_hsps is the maximum number of HSPs (alignments) to \
            keep for any single query-subject pair."
    )
    parser.add_argument(
        "-cl",
        "--culling-limit",
        type = int,
        required = False,
        metavar = "INT",
        default =10,
        help = "Integer value used as threshold for the culling_limit \
            parameter in BLAST. The culling_limit deletes hits that are \
            enveloped by at least this many higher-scoring hits."
    )
    
    parser.add_argument(
        "-c",
        "--cores",
        type = int,
        metavar = "INT",
        default = 300,
        help="Number of cores to use. Default is 300"
    )
    #TODO: Get from ${irods_runsheet_sys__runsheet__lsf_queue} if it exists
    parser.add_argument(
        "-q",
        "--queue",
        type = str,
        metavar = "STR",
        default = 'bio',
        help = 'Name of the queue that the job will be submitted to if working on a cluster. Default is "bio" (normal one at RIVM).'
    )
    parser.add_argument(
        "-l",
        "--local",
        action='store_true',
        help="Running pipeline locally (instead of in a computer cluster). Default is running it in a cluster."
    )
    # Snakemake arguments
    parser.add_argument(
        "-sh",
        "--snakemake_help",
        action = 'store_true',
        help = "Print Snakemake help (passed to snakemake)."
    )
    parser.add_argument(
        "-u",
        "--unlock",
        action = 'store_true',
        help = "Unlock output directory (passed to snakemake)."
    )
    parser.add_argument(
        "-n",
        "--dryrun",
        action='store_true',
        help="Dry run printing steps to be taken in the pipeline without actually running it (passed to snakemake)."
    )
    parser.add_argument(
        "--rerunincomplete",
        action='store_true',
        help="Re-run jobs if they are marked as incomplete (passed to snakemake)."
    )
    args = parser.parse_args()
    JunoBlastRun(input_dir=args.input, 
                output_dir=args.output, 
                evalue=args.evalue,
                max_hsps=args.max_hsps,
                culling_limit=args.culling_limit,
                db_dir = args.db_dir, 
                cores=args.cores,
                local=args.local,
                queue=args.queue,
                unlock=args.unlock,
                rerunincomplete=args.rerunincomplete,
                dryrun=args.dryrun
                )
