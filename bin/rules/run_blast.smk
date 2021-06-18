#############################################################################
#####                               BLAST                               #####
#############################################################################

rule download_blast_db:
    output: 
        db = temp(OUT + "/updated_blast.txt")
    log:
        OUT + "/log/updated_blast.log"
    benchmark:
        OUT + "/log/benchmark/updated_blast.txt"
    threads: config["threads"]["blast"]
    resources: mem_mb=config["mem_mb"]["blast"]
    params:
        db_dir = config["blast_db"]
    shell:
        """
LOG=$(realpath {log})
current_dir=$(pwd)
mkdir -p {params.db_dir}
cd {params.db_dir}
update_blastdb.pl --decompress nt --num_threads {threads} > ${{LOG}}
cd ${{current_dir}}
touch {output}
        """


rule run_blast:
    input:
        assembly = lambda wildcards: SAMPLES[wildcards.sample]["assembly"],
        db_update = OUT + "/log/updated_blast.log"
    output:
        asn = OUT + "/{sample}_blastresults.asn"
    # conda:
    #     "../../envs/mlst7.yaml"
    log:
        OUT + "/log/blast_{sample}.log"
    benchmark:
        OUT + "/log/benchmark/blast_{sample}.txt"
    threads: config["threads"]["blast"]
    resources: mem_mb=config["mem_mb"]["blast"]
    params:
        db_dir = config["blast_db"]
    shell:
        """
blastn -query {input.assembly} -db {params.db_dir}/nt -outfmt 11 -out {output} -num_threads {threads} > {log}
        """