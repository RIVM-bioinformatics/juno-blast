#############################################################################
#####                               BLAST                               #####
#############################################################################

# rule download_blast_db:
#     output: 
#         db = temp(OUT + "/updated_blast.txt")
#     log:
#         OUT + "/log/updated_blast.log"
#     benchmark:
#         OUT + "/log/benchmark/updated_blast.txt"
#     threads: config["threads"]["blast"]
#     resources: mem_mb=config["mem_mb"]["blast"]
#     params:
#         db_dir = config["blast_db"]
#     shell:
#         """
# LOG=$(realpath {log})
# current_dir=$(pwd)
# mkdir -p {params.db_dir}
# cd {params.db_dir}
# update_blastdb.pl --decompress nt --num_threads {threads} > ${{LOG}}
# cd ${{current_dir}}
# touch {output}
#         """


rule run_blast:
    input:
        assembly = lambda wildcards: SAMPLES[wildcards.sample]["assembly"]
    output:
        asn = OUT + "/{sample}_blastresults.asn"
    log:
        OUT + "/log/blast_{sample}.log"
    benchmark:
        OUT + "/log/benchmark/blast_{sample}.txt"
    threads: config["threads"]["blast"]
    resources: mem_gb=config["mem_gb"]["blast"]
    params:
        db_dir = config["blast_db"],
        evalue=config['blast_parameters']['evalue'],
        max_hsps=config['blast_parameters']['max_hsps'],
        culling_limit=config['blast_parameters']['culling_limit']
    shell:
        """
blastn -db {params.db_dir}/nt \
        -query {input.assembly} \
        -out {output} \
        -outfmt "7 qseqid sseqid sscinames sblastnames salltitles sgi pident length mismatch gapopen qstart qend sstart send evalue bitscore" \
        -evalue {params.evalue} \
        -max_hsps {params.max_hsps} \
        -culling_limit 10 \
        -num_threads {threads} > {log}
        """
# blastn -query {input.assembly} -db {params.db_dir}/nt -outfmt 11 -out {output} -num_threads {threads} > {log}
# -max_target_seqs {params.max_target_seqs} \
