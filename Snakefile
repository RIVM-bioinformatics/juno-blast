"""
Juno-typing
Author(s): Alejandra Hernandez-Segura
Organization: Rijksinstituut voor Volksgezondheid en Milieu (RIVM)
Department: Infektieziekteonderzoek, Diagnostiek en Laboratorium Surveillance (IDS), Bacteriologie (BPD)
Date: 17-06-2021
Documentation: 
Snakemake rules (in order of execution):
    1. BLAST
"""
#################################################################################
##### Import config file, sample_sheet and set output folder names          #####
#################################################################################

import os
import yaml


#################################################################################
#####     Load samplesheet, load genus dict and define output directory     #####
#################################################################################

# Loading sample sheet as dictionary 
# ("R1" and "R2" keys for fastq, and "assembly" for fasta)
sample_sheet = config["sample_sheet"]
SAMPLES = {}
with open(sample_sheet) as sample_sheet_file:
    SAMPLES = yaml.safe_load(sample_sheet_file) 

# OUT defines output directory for most rules.
OUT = config["out"]


#@################################################################################
#@####                              Processes                                #####
#@################################################################################

include: "bin/rules/run_blast.smk"

#@################################################################################
#@####              Finalize pipeline (error/success)                        #####
#@################################################################################

onerror:
    shell("""
        echo -e "Something went wrong with Juno-typing pipeline. Please check the logging files in {OUT}/log/"
        """)


onsuccess:
    shell("""
        echo -e "\tGenerating Snakemake report..."
        snakemake --config sample_sheet={sample_sheet} \
                    --configfile config/pipeline_parameters.yaml config/user_parameters.yaml \
                    --cores 1 --unlock
        snakemake --config sample_sheet={sample_sheet} \
                    --configfile config/pipeline_parameters.yaml config/user_parameters.yaml \
                    --cores 1 --report '{OUT}/audit_trail/snakemake_report.html'
        """)


#################################################################################
#####                       Specify final output                            #####
#################################################################################

localrules:
    all

rule all:
    input:
        expand(OUT + "/{sample}_blastresults.asn", sample = SAMPLES)


