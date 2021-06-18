import os
import pathlib
from sys import path
import unittest

main_script_path = str(pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent.absolute())
path.insert(0, main_script_path)
from bin import general_juno_pipeline
import juno_blast



class TestPipelineStartup(unittest.TestCase):
    """Testing the pipeline startup (generating dict with samples) from general Juno pipelines"""
    
    def setUpClass(): 
        """Making fake directories and files to test different case scenarios for starting pipeline"""

        fake_dirs = ['fake_dir_empty', 
                    'fake_dir_wsamples', 
                    'fake_dir_juno', 
                    'fake_dir_juno/clean_fastq', 
                    'fake_dir_juno/de_novo_assembly_filtered']

        fake_files = ['fake_dir_wsamples/sample2_R2_filt.fq.gz', 
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
        """Removing fake directories/files"""

        fake_dirs = ['fake_dir_empty', 
                    'fake_dir_wsamples', 
                    'fake_dir_juno', 
                    'fake_dir_juno/clean_fastq', 
                    'fake_dir_juno/de_novo_assembly_filtered']

        for folder in fake_dirs:
            os.system('rm -rf {}'.format(str(folder)))

    def test_emptydir(self):
        """Testing the pipeline startup fails if the input directory does not have expected files"""
        self.assertRaises(ValueError, general_juno_pipeline.PipelineStartup, pathlib.Path('fake_dir_empty'), 'both')

    def test_correctdir_wdifffastqextensions(self):
        """Testing the pipeline startup accepts fastq and fastq.gz files"""

        expected_output = {'sample1': {'assembly': 'fake_dir_wsamples/sample1.fasta'}, 
                            'sample2': {'assembly': 'fake_dir_wsamples/sample2.fasta'}}
        pipeline = general_juno_pipeline.PipelineStartup(pathlib.Path('fake_dir_wsamples'), 'fasta')
        self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_junodir_wnumericsamplenames(self):
        """Testing the pipeline startup converts numeric file names to string"""

        expected_output = {'1234': {'assembly': 'fake_dir_juno/de_novo_assembly_filtered/1234.fasta'}}
                
        pipeline = general_juno_pipeline.PipelineStartup(pathlib.Path('fake_dir_juno'), 'fasta')
        self.assertDictEqual(pipeline.sample_dict, expected_output)

    def test_string_accepted_as_inputdir(self):
        """Testing the pipeline startup accepts string (not only pathlib.Path) as input"""

        expected_output = {'1234': {'assembly': 'fake_dir_juno/de_novo_assembly_filtered/1234.fasta'}}
                
        pipeline = general_juno_pipeline.PipelineStartup('fake_dir_juno', 'fasta')
        self.assertDictEqual(pipeline.sample_dict, expected_output)



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
        raised = False
        try:
            juno_blast.JunoBlastRun(input_dir = 'fake_dir_wsamples', 
                                    output_dir = pathlib.Path('output'), 
                                    db_dir = pathlib.Path('fake_db'),
                                    dryrun = True)
        except:
            raised = True
            raise
        self.assertFalse(raised, 'Exception raised when running a dryrun')



@unittest.skipIf(not pathlib.Path('/mnt/db/juno/blast/').exists(),
                     "Skipped in non-RIVM environments")
class TestJunoBlastPipeline(unittest.TestCase):
    """Testing the JunoBlast class (code specific for this pipeline)"""

    def setUpClass():
        os.system('rm -rf test_output')

    def tearDownClass():
        os.system('rm -rf test_output')
    
    def test_junoblast_run(self):
        """Testing the pipeline runs properly in test data"""
        raised = False
        try:
            juno_blast.JunoBlastRun(input_dir = 'tests/sample_test', 
                                    db_dir = "/mnt/db/juno/blast",
                                    local = False,
                                    cores = 6,
                                    output_dir = pathlib.Path('test_output'),
                                    dryrun = False)
        except:
            raised = True
            raise
        main_script_path = pathlib.Path(pathlib.Path(__file__).parent.absolute()).parent.absolute()
        self.assertFalse(raised, 'Exception raised when running Juno_blast')
        self.assertTrue(main_script_path.joinpath('test_output', 'fasta_example_blastresults.asn').is_file())



if __name__ == '__main__':
	unittest.main()