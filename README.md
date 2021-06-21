<div align="center">
    <h1>Juno-blast</h1>
    <br />
    <h2>Automated BLASTing from fasta files.</h2>
    <br />
    <img src="https://via.placeholder.com/150" alt="pipeline logo">
</div>

## Pipeline information

* **Author(s):**            Alejandra Hernández Segura
* **Organization:**         Rijksinstituut voor Volksgezondheid en Milieu (RIVM)
* **Department:**           Infektieziekteonderzoek, Diagnostiek en Laboratorium Surveillance (IDS), Bacteriologie (BPD)
* **Start date:**           17 - 06 - 2021
* **Commissioned by:**      Antoni Hendrickx and Varisha Ganesh

## About this project

This is a short pipeline that takes (multi) fasta files as input containing one or more DNA-sequences. These sequences are then BLASTed against a local copy of the 'nt' database from BLAST. Before running BLAST, the pipeline will download/update the database if necessary so that the last version of it is used. 

## Prerequisities

* **Linux + conda** A Linux-like environment with at least 'miniconda' installed. 
* **Python3.7.6** .


## Installation

1. Clone the repository:

```
git clone https://github.com/RIVM-bioinformatics/Juno_blast.git
```
Alternatively, you can download it manually as a zip file (you will need to unzip it then).

2. Enter the directory with the pipeline and install the master environment:

```
cd Juno_blast
conda env install -f envs/master_env.yaml
```

## Parameters & Usage

### Command for help

* ```-h, --help``` Shows the help of the pipeline

### Required parameters

* ```-i, --input``` Directory with the input (fasta) files. The fasta files should be all in this directory (no subdirectories) and have the extension '.fasta'. 

### Optional parameters

* ```-o --output``` Directory (if not existing it will be created) where the output of the pipeline will be collected. The default behavior is to create a folder called 'output' within the pipeline directory. 
* ```-d --db_dir``` Directory (if not existing it will be created) where the output of the pipeline will be collected. The default behavior is to create a folder called 'output' within the pipeline directory. Default is '/mnt/db/juno/blast' (RIVM path to the databases of the Juno pipelines). It is advisable to provide your own path if you are not working inside the RIVM Linux environment.
* ```-c --cores```  Maximum number of cores to be used to run the pipeline. Defaults to 300 (it assumes you work in an HPC cluster).
* ```-l --local```  If this flag is present, the pipeline will be run locally (not attempting to send the jobs to a cluster). Keep in mind that if you use this flag, you also need to adjust the number of cores (for instance, to 2) to avoid crashes. The default is to assume that you are working on a cluster because the pipeline was developed in an environment where it is the case.
* ```-q --queue```  If you are running the pipeline in a cluster, you need to provide the name of the queue. It defaults to 'bio' (default queue at the RIVM). 
* ```-n --dryrun```, ```-u --unlock``` and ```--rerunincomplete``` are all parameters passed to Snakemake. If you want the explanation of these parameters, please refer to the [Snakemake documentation](https://snakemake.readthedocs.io/en/stable/).


### The base command to run this program (for people at the RIVM). 

```
python juno_blast.py -i [dir/to/input_directory]
```

### An example on how to run the pipeline.

```
python juno_blast.py -i my_input_files -o my_results --local --cores 2
```

## Explanation of the output

* **log:** Log files with output and error files from each Snakemake rule/step that is performed. 
* **output** One output file (.asn extension) per sample will be created containing the BLAST results.

## Issues  

* All default values have been chosen to work with the RIVM Linux environment, therefore, there might not be applicable to other environments (although they should work with the appropriate arguments/parameters).
* Any issue can be reported in the [Issues section](https://github.com/RIVM-bioinformatics/Juno_blast/issues) of this repository.

## Future ideas for this pipeline

* Have a separate script to update/download the database so that the pipeline is not slowed down by this step.  
* Producing an output that is easier to explore/navigate. 

## License
This pipeline is licensed with an AGPL3 license. Detailed information can be found inside the 'LICENSE' file in this repository.

## Contact
* **Contact person:**       Alejandra Hernández Segura
* **Email**                 alejandra.hernandez.segura@rivm.nl
