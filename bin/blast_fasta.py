# from Bio.Blast import NCBIWWW
# from Bio.Blast import NCBIXML
# from Bio.Blast.Applications import NcbiblastxCommandline
import pathlib
import subprocess
import uuid





def run_blast(fasta, 
                database_path,
                expect = 10.0,
                alignments = 500,
                descriptions = 500,
                threads = 1):
    """Run BLAST on the provided fasta file""" 

    fasta = pathlib.Path(fasta)
    database_path = pathlib.Path(database_path)
    assert fasta.is_file(), "The provided fasta file does not exist".format(str(fasta))
    assert database_path.is_dir(), "The provided path to the Blast database does not exist".format(str(database_path))
    assert database_path.joinpath('nt.00.nhi').is_file(), "The provided path to the Blast database ({}) does not contain all the necessary files. Please download the Blast database again.".format(str(database_path))

    output_asn = fasta.with_suffix('.asn')
    jobid = "blast" + str(uuid.uuid4())[-6:]

    print("Running blast")
    subprocess.check_call("bsub -n {num_threads} -q bio -J {jobid} blastn -query {query} -db {db}/nt -outfmt 11 -out {out} -num_threads {num_threads} >> data_log.txt 2>&1 && sleep 10".format(query = fasta,
                                                                                                                                                                db = database_path,
                                                                                                                                                                out = output_asn,
                                                                                                                                                                outfmt = 11,
                                                                                                                                                                num_threads = threads,
                                                                                                                                                                jobid = jobid), 
                            shell=True)
    print("Waiting")
    subprocess.check_call('bwait -w "ended({jobid})"'.format(jobid = jobid))

    # subprocess.check_call('blast_formatter -archive {archive} -outfmt "7 qacc sacc evalue qstart qend sstart send"'.format(archive = output_asn), 
    #                         shell=True)

    return str(output_asn)

def filter_blast_result():
    E_VALUE_THRESH = 1e-20 
    for record in NCBIXML.parse(open("tests/fasta_example.xml")): 
        if record.alignments: 
            print("\n") 
            print("query: %s" % record.query[:100]) 
        for align in record.alignments: 
            for hsp in align.hsps: 
                if hsp.expect < E_VALUE_THRESH: 
                    print("match: %s " % align.title[:100])




if __name__ == '__main__':
    # parser = argparse.ArgumentParser(
    #     description = "Juno-typing pipeline. Automated pipeline for bacterial subtyping (7-locus MLST and serotyping)."
    # )
    # parser.add_argument(
    #     "-i",
    #     "--input",
    #     type = pathlib.Path,
    #     required = True,
    #     metavar = "DIR",
    #     help = "Relative or absolute path to the input directory. It must either be the output directory of the Juno-assembly pipeline or it must contain all the raw reads (fastq) and assemblies (fasta) files for all samples to be processed."
    # )
    # parser.add_argument(
    #     "-m",
    #     "--metadata",
    #     type = pathlib.Path,
    #     default = None,
    #     metavar = "FILE",
    #     help = "Relative or absolute path to the metadata csv file. If provided, it must contain at least one column with the 'Sample' name (name of the file but removing _R1.fastq.gz), a column called 'Genus' and a column called 'Species'. If a genus + species is provided for a sample, the MLST7 is not run."
    # )
    run_blast(fasta = "tests/fasta_example.fasta", 
                database_path = "db_v4",
                expect = 10.0,
                alignments = 500,
                descriptions = 500,
                threads = 4)