import os
import pathlib
import subprocess
from sys import path
import unittest

main_script_path = str(pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent.absolute())
path.insert(0, main_script_path)
import juno_blast

class TestJunoBlastDryRun(unittest.TestCase):
    """Testing the JunoBlast class (code specific for this pipeline)"""

    def setUpClass():
        fake_dirs = ['fake_dir_wsamples', 
                    'fake_dir_juno', 
                    'fake_dir_juno/clean_fastq', 
                    'fake_dir_juno/de_novo_assembly_filtered']

        fake_files = ['fake_dir_wsamples/sample1_R1.fastq',
                    'fake_dir_wsamples/sample1_R2.fastq.gz',
                    'fake_dir_wsamples/sample2_R1_filt.fq',
                    'fake_dir_wsamples/sample2_R2_filt.fq.gz', 
                    'fake_dir_wsamples/sample1.fasta',
                    'fake_dir_wsamples/sample2.fasta',
                    'fake_dir_juno/clean_fastq/1234_R1.fastq.gz',
                    'fake_dir_juno/clean_fastq/1234_R2.fastq.gz', 
                    'fake_dir_juno/de_novo_assembly_filtered/1234.fasta']
                            
        for folder in fake_dirs:
            pathlib.Path(folder).mkdir(exist_ok = True)
        for file_ in fake_files:
            pathlib.Path(file_).touch(exist_ok = True)

    def tearDownClass():
        fake_dirs = ['fake_dir_wsamples', 
                    'fake_dir_juno']
        for folder in fake_dirs:
            os.system('rm -rf {}'.format(str(folder)))
    
    def test_junotyping_dryrun(self):
        """Testing the pipeline runs properly as a dry run"""
        juno_blast_run = juno_blast.JunoBlastRun(input_dir = 'fake_dir_wsamples', 
                                                output_dir = pathlib.Path('output'), 
                                                db_dir = pathlib.Path('fake_db'),
                                                dryrun = True)
        self.assertTrue(juno_blast_run.successful_run, 
                        'Exception raised when running a dryrun')



@unittest.skipIf(not pathlib.Path('/mnt/db/Jovian/NT_database').exists(),
                     "Skipped in non-RIVM environments")
class TestJunoBlastPipeline(unittest.TestCase):
    """Testing the JunoBlast class (code specific for this pipeline)"""

    def setUpClass():
        os.system('rm -rf test_output')

    def tearDownClass():
        os.system('rm -rf test_output')
    
    def test_junoblast_run(self):
        """Testing the pipeline runs properly in test data"""
        output_dir = pathlib.Path('test_output')
        juno_blast_run = juno_blast.JunoBlastRun(input_dir = 'tests/sample_test', 
                                    db_dir = "/mnt/db/Jovian/NT_database",
                                    local = False,
                                    cores = 6,
                                    output_dir = output_dir,
                                    dryrun = False)
        expected_result_file = output_dir.joinpath('fasta_example_blastresults.asn')
        
        self.assertTrue(juno_blast_run.successful_run, 
                        'Exception raised when running a dryrun')
        self.assertTrue(expected_result_file.is_file())
        actual_result=subprocess.check_output(['grep', 
                                                '10 hits', 
                                                f'{str(expected_result_file)}'])
        expected_result = b'# 10 hits found\n# 10 hits found\n# 10 hits found\n'
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
	unittest.main()