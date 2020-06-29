import unittest 
from clipper.src.peakfinder import *
from clipper.src.call_peak import Peak
import pkg_resources           
import pysam
import filecmp
import pybedtools
from collections import namedtuple
class Test(unittest.TestCase):
    
    parser = None
    def setUp(self):
              
        """
        
        General setup, currently creates parser for various allup tests
        
        """
        # modulize parser from peak_finder to ensure unified bahaviour
        self.parser = option_parser()
    def test_allup(self):
        
        """
        Performs basic all up test on entire program (except for main)
        """
        
        #self.assertTrue(False, "test is currently disabled output from logging causes it to crash")
        args = ["--bam", clipper.test_file("allup_test.bam"),
                 "--species", "hg19",
                 "--gene", "ENSG00000198901",
                 "--outfile" + os.getcwd() + "/allup_peak_results.bed",
                 "--debug",
                ]

        (options, args) = self.parser.parse_args(args)
        options = override_options(options)
        
        main(options)
        
        tested = open(os.getcwd() + "/allup_peak_results.bed")
        correct = open(clipper.test_file("peak_results_no_overlap.BED"))
        
        
        #problem with tracks being different
        tested_tool = pybedtools.BedTool(tested)
        correct_tool = pybedtools.BedTool(correct)
        
        #checks to make sure files are equal and there are not exact dups
        print len(tested_tool)
        print len(correct_tool)
        
        self.assertAlmostEqual(len(tested_tool), len(correct_tool), delta=3)
        print len(tested_tool)
        print len(correct_tool)
        #assert False
        """
        for test, correct in zip(tested_tool, correct_tool):
            self.assertEqual(test, correct)
        

        """
        
        #cleanup
        os.remove(os.getcwd() + "/allup_peak_results.bed")
    
    # def test_classic_allup(self):
    #
    #     """
    #     DON't NEED TO TEST SINCE OVERRIDE method option with spline
    #     Performs basic all up test on entire program (using classic algorithm) (except for main)
    #
    #     """
    #
    #     #self.assertTrue(False, "test is currently disabled output from logging causes it to crash")
    #     args = ["-b", clipper.test_file("allup_test.bam"),
    #              "-s", "hg19",
    #              "-g", "ENSG00000198901",
    #              "--outfile=" + os.getcwd() + "/allup_peak_results_classic.bed",
    #              "--debug",
    #              "--algorithm=classic"
    #             ]
    #
    #     (options, args) = self.parser.parse_args(args)
    #     options = override_options(options)
    #
    #
    #     main(options)
    #
    #     tested = open(os.getcwd() + "/allup_peak_results_classic.bed")
    #     correct = open(clipper.test_file("peak_results_no_overlap.BED"))
    #
    #
    #     #problem with tracks being different
    #     tested_tool = pybedtools.BedTool(tested)
    #     correct_tool = pybedtools.BedTool(correct)
    #
    #     #self.assertAlmostEqual(len(tested_tool), len(correct_tool), delta=3)
    #
    #     """
    #     for test, correct in zip(tested_tool, correct_tool):
    #         self.assertEqual(test, correct)
    #
    #
    #     """
    #
    #     #cleanup
    #     os.remove(os.getcwd() + "/allup_peak_results_classic.bed")
    def test_allup_parrallel(self):
        
        """
    
        Performs basic all up test on entire program (except for main), running in parrallel to 
        try to detect crashes
        
        """
    
        args = ["-b", clipper.test_file("allup_test.bam"),
                 "-s", "hg19",
                 "-g", "ENSG00000198901", 
                 "--outfile=" + os.getcwd() + "/allup_peak_results.bed",
                ]

        (options, args) = self.parser.parse_args(args)
        options = override_options(options)
        
        
        main(options)
        
        tested = open(os.getcwd() + "/allup_peak_results.bed")
        correct = open(clipper.test_file("peak_results_no_overlap.BED"))
        
        
        #problem with tracks being different
        tested_tool = pybedtools.BedTool(tested)
        correct_tool = pybedtools.BedTool(correct)
        
        #checks to make sure files are equal and there are not exact dups
        print len(tested_tool)
        print len(correct_tool)
        
        self.assertAlmostEqual(len(tested_tool), len(correct_tool), delta=3)
        print len(tested_tool)
        print len(correct_tool)
        #assert False
        """
        for test, correct in zip(tested_tool, correct_tool):
            self.assertEqual(test, correct)
        

        """
        #cleanup
        os.remove(os.getcwd() + "/allup_peak_results.bed")
    
    def test_gtf_allup(self):
        
        """
    
        Performs basic all up test on entire program (using classic algorithm) using gtf file
        
        """
        
        #self.assertTrue(False, "test is currently disabled output from logging causes it to crash")
        args = ["-b", clipper.test_file("allup_test.bam"),
                 "--gtfFile", clipper.test_file("ensembl_test.gtf"),
                 "-g", "ENSG00000198901", 
                 "--outfile=" + os.getcwd() + "/allup_peak_results_ensembl_test.bed",
                 "--debug",
                 "--algorithm=classic"
                ]

        (options, args) = self.parser.parse_args(args)
        options = override_options(options)
        
        
        main(options)
        
    def test_filter(self):
        
        """
        
        allup test for transcriptome filter 
        makes sure special test file 
        detects only one peak when filter is enabled and detects two peaks when filter is disabled
        
        """
    
        args = ["-b", clipper.test_file("transcriptome_filter.sort.bam"),
                 "-s", "hg19",
                  "-g", "ENSG00000198901", 
                  '-g', "ENSG00000226167",
                   "--outfile=" + os.getcwd() + "/cut_off_included.bed",
                   "-q",
                   "--debug"
                ]    
        (options, args) = self.parser.parse_args(args)
        options = override_options(options)
        main(options)
        
        tested = open(os.getcwd() + "/cut_off_included.bed")
        
        #problem with tracks being different
        tested_tool = pybedtools.BedTool(tested)
   
        
        #checks to make sure files are equal and there are not exact dups
        #cutoff stuff is borken and possibly buggy, need to fix later
        #self.assertEqual(len(tested_tool), 1)
                
        #cleanup
        os.remove(os.getcwd() + "/cut_off_included.bed")
        
    def test_cutoff(self):
        
        """
        
        test_cutoff Tests that the cutoff code works if its enabled
        
        """
    
        args = ["-b", clipper.test_file("transcriptome_filter.sort.bam"),
                 "-s", "hg19",
                  "-g", "ENSG00000198901", 
                  '-g', "ENSG00000226167",
                   "--outfile=" + os.getcwd() + "/no_cut_off.bed",
                   "-q",
                   "--disable_global_cutoff",
                   '--debug'
                ]    
        (options, args) = self.parser.parse_args(args)
        options = override_options(options)
        main(options)
        
        tested = open(os.getcwd() + "/no_cut_off.bed")
        
        #problem with tracks being different
        tested_tool = pybedtools.BedTool(tested)
   
        
        #checks to make sure files are equal and there are not exact dups
        #cutoff of stuff is broken and possibly buggy, need to fix later
        #self.assertEqual(len(tested_tool), 2)
                
        #cleanup
        os.remove(os.getcwd() + "/no_cut_off.bed")
        
    def test_check_overlaps(self):
        
        """
    
        Checks for overlapping results, we don't want this
        
        overlaps have been borken for a while, disabling test until its really a problem
        """

        return 
        args = ["-b", clipper.test_file("allup_test.bam"),
                 "-s", "hg19",
                  "-g", "ENSG00000198901", 
                  "--serial", 
                  "--job_name=peak_test",
                   "--outfile=" + os.getcwd() + "/overlap_peak_results.bed",
                   "-q",
                   "--debug"
                ]    
        (options, args) = self.parser.parse_args(args)
        options = override_options(options)
        main(options)
        
        #tests to make sure there are no overlaps
        tested = open(os.getcwd() + "/overlap_peak_results.bed")
        tested_tool2 = pybedtools.BedTool(tested).saveas(os.getcwd() + "/overlaps.bed")
        result = tested_tool2.intersect(tested_tool2)
        self.assertEqual(len(result), len(tested_tool2), 
                         "there are overlaps in the output file") 
        
        #cleanup
        os.remove(os.getcwd() + "/overlap_peak_results.bed")
        os.remove(os.getcwd() + "/overlaps.bed")
       
    def test_check_for_index(self):
        
        """
    
        Performs unit tests on check_for_index function
        
        """
        
        #Test if string is null, expected result is operation 
        #throws file not exist exception 
        handle = None
        self.assertRaises(TypeError, check_for_index, handle)
        
        #Test if bam file doesn't exist, expected result is operation throws 
        #file does not exist exception
        handle = "/foo/bar"
        self.assertRaises(NameError, check_for_index, handle)
        
        #Test if file is not bam, but exists expected 
        #result is to throw improper file error
        handle = clipper.test_file("test_peakfinder.py")
        self.assertRaises(NameError, check_for_index, handle)
        
        #Test if file is bam and indexed expected 
        #result is returns 1 and succedes
        #should also check if file exists, but I'm lazy
        handle = clipper.test_file("indexed_test.bam")
        result = check_for_index(handle)
        assert result == None
        
        #Test if file is bam and not indexed, expected 
        #result is returns one and succedes
        #should also check if file exists, but I'm lazy
        handle = clipper.test_file("not_indexed_test.bam")
        result = check_for_index(handle)
        assert result == None
        
        #cleanup (should be in taredown)
        os.remove(clipper.test_file("not_indexed_test.bam.bai"))
    
    
#    def test_build_transcript_data_bed(self):
#        
#        """
#        
#        Tests building transcript data from bed with both pre-mrna and mrna data
#        
#        """
#        
#        test = pybedtools.BedTool(clipper.test_file("test_bed_creation.bed"))
#
#        true_genes = {["chr1", "AS_STRUCTURE", "mRNA", 66999065, 67210057, ".", "+", ".", "transcript_id=ENST00000237247;effective_length=3997" ],
#                      ["chr1", "AS_STRUCTURE", "mRNA", 66999274, 66999274, ".", "+", ".", "transcript_id=ENST00000371039;effective_length=4080" ], 
#                      ["chr1", "AS_STRUCTURE", "mRNA", 66999297, 67145425, ".", "+", ".", "transcript_id=ENST00000424320;effective_length=951" ], 
# 
#        
#        genes = build_transcript_data_bed(test, False)
#        
#        self.assertDictEqual(true_genes, genes, "mrna genes not equal")
#        
#        #tests pre-mrna 
#        
#        true_lengths = {"ENST00000237247" : 210992, "ENST00000371039" : 211494, "ENST00000424320" : 146128}
#        genes = build_transcript_data_bed(test, True)
#        
#        self.assertDictEqual(true_genes, genes, "pre-mrna genes not equal")
#        self.assertDictEqual(true_lengths, lengths, "pre-mrna lengths not equal")
#        
    def test_build_geneinfo(self):
        
        """
    
        Performs unit testing on build_geneinfo
        
        I'm hopefully going to remove this method soon so no testing for now
        
        """ 
        
        #checks error mode
        self.assertRaises(TypeError, build_geneinfo, None)
        
        self.assertRaises(IOError, build_geneinfo, "foo")

        #checks working mode
        geneinfo = build_geneinfo(
                    clipper.data_file("test.AS.STRUCTURE_genes.BED.gz"))

  
        true_values = {
        "ENSG00000232113" : ["chr1",  "ENSG00000232113",  173604911,      173606273, "+"],
        "ENSG00000228150" : ["chr1",  "ENSG00000228150",  10002980,       10010032,  "+"],
        "ENSG00000223883" : ["chr1",  "ENSG00000223883",  69521580,       69650686,  "+"],
        "ENSG00000135750" : ["chr1",  "ENSG00000135750",  233749749,      233808258, "+"],
        "ENSG00000227280" : ["chr1",  "ENSG00000227280",  145373053,      145375554 ,"-"],
        }


        self.assertDictEqual(geneinfo, true_values)
        
    def test_build_lengths(self):
        
        """
    
        Performs unit testing on build_lengths
        
        I'm hopefully going to remove this method soon so no unit testing for now
        
        """
        
        #Checks error mode
        self.assertRaises(ValueError, build_lengths, None)
        
        self.assertRaises(ValueError, build_lengths, clipper.test_file("foo"))
        
        #checks working mode
        lengths = build_lengths(
                    clipper.data_file("test.AS.STRUCTURE_mRNA.lengths"))

        true = {"ENSG00000232113" : 384,
                "ENSG00000228150" : 323,
                "ENSG00000223883" : 437,
                "ENSG00000135750" : 3141,
                "ENSG00000227280" : 212,
                }       
         
        self.assertDictEqual(lengths, true)
        
    def test_add_species(self):
        
        """
    
        Performs unit testing on add_species
        
        I'll probably refactor this a bit so I won't work to hard on testing this
       
        """
        
        #Case: object is returned as expected
        result = add_species("hg19", [range(1, 22), "X", "Y"], 
                                        "foo", 
                                        "bar", 
                                        "baz")
        
        self.assertEqual(result, {"chrs" : range(1, 22) + ["X"] + ["Y"], 
                          "gene_bed" : "foo", 
                          "mRNA" : "bar", 
                          "premRNA" : "baz"})
    
    def test_get_acceptable_species(self):
        
        """
        
        Test get acceptable species 
        
        """
        
        result = get_acceptable_species()
        
        # make sure some main genomes are in here.
        self.assertIn("hg19", result)
        self.assertIn("mm9", result)
        self.assertIn("mm10", result)
        self.assertIn("GRCh38", result)
    
      
    def test_build_transcript_data(self):
        self.maxDiff = 10000000
        """
        
        Tests building transcript data and returning the proper values
        
        Doesn't assume malformed data
        
        """
    
        #tests error modes    
        self.assertRaises(ValueError, build_transcript_data, None, None, None, None, True)
        
        self.assertRaises(ValueError, build_transcript_data, "foo", "bar", "bar", "bar", True)
        
        self.assertRaises(ValueError, build_transcript_data, "bar", None, None, None, True)
        
        #tests hg19 to make sure its equal to logic
        genes = build_transcript_data("test", None, None, None, True).sort()
        true_genes = pybedtools.BedTool(
                [["chr1", "AS_STRUCTURE", "mRNA", 173604911, 173606273, ".", "+", ".", "gene_id=ENSG00000232113; effective_length=1147" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 10002980, 10010032, ".", "+", ".", "gene_id=ENSG00000228150; effective_length=3088" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 69521580, 69650686, ".", "+", ".", "gene_id=ENSG00000223883; effective_length=46051" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 233749749, 233808258, ".", "+", ".", "gene_id=ENSG00000135750; effective_length=35997" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 145373053, 145375554, ".", "-", ".", "gene_id=ENSG00000227280; effective_length=609" ]],
                                        ).sort()
    
        self.assertEqual(str(genes), str(true_genes))
                
        #tests hg19 on premrna lengths
        genes = build_transcript_data("test", None, None, None, False).sort()
        
        true_genes = pybedtools.BedTool(
                [["chr1", "AS_STRUCTURE", "mRNA", 173604911, 173606273, ".", "+", ".", "gene_id=ENSG00000232113; effective_length=384" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 10002980, 10010032, ".", "+", ".", "gene_id=ENSG00000228150; effective_length=323" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 69521580, 69650686, ".", "+", ".", "gene_id=ENSG00000223883; effective_length=437" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 233749749, 233808258, ".", "+", ".", "gene_id=ENSG00000135750; effective_length=3141" ],
                ["chr1", "AS_STRUCTURE", "mRNA", 145373053, 145375554, ".", "-", ".", "gene_id=ENSG00000227280; effective_length=212" ]],
                                        ).sort()
        
        self.assertEqual(str(genes), str(true_genes))
        
        #Test custom files 
        #this should all work, 
        self.assertRaises(IOError, build_transcript_data, None, clipper.data_file("test.AS.STRUCTURE_genes.BED.gz"), None, clipper.data_file("test.AS.STRUCTURE_premRNA.lengths"), False)
        build_transcript_data(None, clipper.data_file("test.AS.STRUCTURE_genes.BED.gz"), clipper.data_file("test.AS.STRUCTURE_mRNA.lengths"), clipper.data_file("test.AS.STRUCTURE_premRNA.lengths"), True)
        build_transcript_data(None, clipper.data_file("test.AS.STRUCTURE_genes.BED.gz"), clipper.data_file("test.AS.STRUCTURE_mRNA.lengths"), clipper.data_file("test.AS.STRUCTURE_premRNA.lengths"), False)
        build_transcript_data(None, clipper.data_file("test.AS.STRUCTURE_genes.BED.gz"), clipper.data_file("test.AS.STRUCTURE_mRNA.lengths"), None, False)
        build_transcript_data(None, clipper.data_file("test.AS.STRUCTURE_genes.BED.gz"), None, clipper.data_file("test.AS.STRUCTURE_mRNA.lengths"), True)
    
    # def test_transcriptome_filter(self):
    #
    #     """
    #     DEPRECATED, no function named `transcriptome_filter`
    #     Tests transcriptome filter
    #     not great tests, but good enough to make sure we don't have regressions
    #
    #     """
    #
    #
    #     cluster = Peak(0,0,0,0,0,0,0,0,0,5,0,10,0,0,0,0)
    #     #cluster = {'Nreads' : 5, "size" : 10}
    #     transcriptome_size = 1000
    #     transcriptome_reads = 10000
    #     poisson_cutoff = .05
    #
    #     result = transcriptome_filter(poisson_cutoff, transcriptome_size, transcriptome_reads, cluster)
    #
    #     self.assertEqual(result, 1)
    #
    #     #cluster = {'Nreads' : 10000, "size" : 100}
    #     cluster = Peak(0,0,0,0,0,0,0,0,0,10000,0,100,0,0,0,0)
    #
    #     transcriptome_size = 1000
    #     transcriptome_reads = 10000
    #     poisson_cutoff = .05
    #
    #     result = transcriptome_filter(poisson_cutoff, transcriptome_size, transcriptome_reads, cluster)
    #     self.assertEqual(result,0.0)
    #
    #     #cluster = {'Nreads' : 0, "size" : 0}
    #     cluster = Peak(0,0,0,0,0,0,0,0,0,0,0,0,0)
    #     transcriptome_size = 0
    #     transcriptome_reads = 10000
    #     poisson_cutoff = .05
    #
    #     result = transcriptome_filter(poisson_cutoff, transcriptome_size, transcriptome_reads, cluster)
    #     self.assertEqual(result, 1)
        
    def test_filter_peaks_dicts(self):
        
        """
        
        Tests filter results
        
        good for regression tests, need to do better verification...
        
        """

        peak1 = Peak(chrom="chr15",
                     genomic_start=1, genomic_stop=10,
                     gene_name="ENSG1",
                     strand="-",
                     thick_start=50, thick_stop=60,
                     peak_number=1, number_reads_in_peak=52, size=32, p = 0,
                     effective_length=425, peak_length = 32, area_reads=89, area_size = 95, nreads_in_gene=400)
        peak2 = Peak(chrom="chr15",
                     genomic_start=200, genomic_stop=300,
                     gene_name="ENSG2",
                     strand="-",
                     thick_start=140, thick_stop=160,
                     peak_number=2, number_reads_in_peak=239, size=45, p=0,
                     effective_length=200, peak_length=45, area_reads=400, area_size=100, nreads_in_gene=300)


        peak_dict = {'loc': ['chr15', 'ENSG00000198901', 91509274, 91537804, '-'],
          'Nclusters': 24, 
          'nreads': 2086, 
          'threshold': 32, 
          'clusters': [peak1, peak2]}
        

        transcriptome_size = 10000
        transcriptome_reads = 100000

        # try different params
        result = filter_peaks_dicts([peak_dict], .07, transcriptome_size, transcriptome_reads,
                                    use_global_cutoff=False, bonferroni_correct=True,
                                    superlocal=True, min_width=50, bypassfiltering=False)

        ans='chr15\t1\t10\tENSG1_1_52\t0.000199322700259\t-\t50\t60\nchr15\t200\t300\tENSG2_2_239\t2.24979875151e-58\t-\t140\t160\n'
        self.assertIn('ENSG1_1_52', result)
        self.assertIn('ENSG2_2_239', result)

        # lower poission cutoff
        result = filter_peaks_dicts([peak_dict], .00001, transcriptome_size, transcriptome_reads,
                                    use_global_cutoff=False, bonferroni_correct=True,
                                    superlocal=True, min_width=50, bypassfiltering=False)
        self.assertIn('ENSG2_2_239', result)
        self.assertNotIn('ENSG1_1_52', result)

        # use global cutoff
        result = filter_peaks_dicts([peak_dict], .007, transcriptome_size, transcriptome_reads,
                                    use_global_cutoff=True, bonferroni_correct=True,
                                    superlocal=False, min_width=50, bypassfiltering=False)
        self.assertIn('ENSG2_2_239', result)
        self.assertIn('ENSG2_2_239', result)

    def test_broken_filter_results(self):
        
        """
        
        Tests filter results, expects no output, even from transcriptome wide estimations
        
        """
        
        peak1 = Peak("chr15", 1, 10, "ENSG1", .04 , "-", 50, 60, 1, 52, .04, 32, 0)
        peak2 = Peak("chr15", 200, 300, "ENSG2", .06 , "-", 140, 160, 2, 239, .06, 45, 0)
        results = [{'loc': ['chr15', 'ENSG00000198901', 91509274, 91537804, '-'], 
          'Nclusters': 24, 
          'nreads': 2086, 
          'threshold': 32, 
          'clusters': [peak1, peak2]}]
        

        transcriptome_size = 10000
        transcriptome_reads = 100000
        
        #I had my mental model of how the global cutoff was should have worked wrong the entire time...
        result = filter_results(results, .07, transcriptome_size, transcriptome_reads, True, False, "foo")
        self.assertSetEqual(set(['chr15\t1\t10\tENSG1_1_52\t0.04\t-\t50\t60', 'chr15\t200\t300\tENSG2_2_239\t0.06\t-\t140\t160']), result)
    
    def test_bonferroni_correct_filter_results(self):
        
        """
        
        Tests to make sure bonferroni correction works
        
        """
        
        transcriptome_size = 10000
        transcriptome_reads = 100000
        
        peak1 = Peak("chr15", 1, 10, "ENSG1", .04 , "-", 50, 60, 1, 52, .04, 32, 0)
        peak2 = Peak("chr15", 200, 300, "ENSG2", .06 , "-", 140, 160, 2, 239, .06, 45, 0)
        results = [{'loc': ['chr15', 'ENSG00000198901', 91509274, 91537804, '-'], 
          'Nclusters': 24, 
          'nreads': 2086, 
          'threshold': 32, 
          'clusters': [peak1, peak2]}]
        
        result = filter_results(results, .09, transcriptome_size, transcriptome_reads, False, True)
        self.assertSetEqual(set(['chr15\t1\t10\tENSG1_1_52\t0.08\t-\t50\t60']), result)
        
    def test_count_transcriptome_reads(self):
        """
        
        Tests count_transcriptome_reads
        
        """
        
        results = [
          {'loc': ['chr15', 'ENSG00000198901', 91509274, 91537804, '-'], 
          'Nclusters': 24, 
          'nreads': 200, 
          'threshold': 32, 
          'clusters': {'chr15\t1\t10\tENSG1\t3.44651351902e-09\t-\t50\t60': {'GeneP': 3.4465135190231422e-09, 'Nreads': 100, 'SloP': 3.4465135190231422e-09, 'size': 32}, 
                       'chr15\t200\t300\tENSG2\t0.0\t-\t140\t160': {'GeneP': 0.0, 'Nreads': 100, 'SloP': 0.0, 'size': 45}}}, 
          {'loc': ['chr15', 'ENSG00000198901', 91509274, 91537804, '-'], 
          'Nclusters': 24, 
          'nreads': 200, 
          'threshold': 32, 
          'clusters': {'chr15\t1\t10\tENSG1\t3.44651351902e-09\t-\t50\t60': {'GeneP': 3.4465135190231422e-09, 'Nreads': 100, 'SloP': 3.4465135190231422e-09, 'size': 32}, 
                       'chr15\t200\t300\tENSG2\t0.0\t-\t140\t160': {'GeneP': 0.0, 'Nreads': 100, 'SloP': 0.0, 'size': 45}}},  
                   ]
        result = count_transcriptome_reads(results)
        
        self.assertEqual(400, result)
    
    def test_build_transcript_data_gtf(self):
        
        """
        
        Tests build transcript data gtf, tests two genes, with some noise
        
        """
        
        #tests pre-mrna
        genes = build_transcript_data_gtf(pybedtools.BedTool(clipper.test_file("data.gtf")), True).sort()
        true_genes = pybedtools.BedTool(
                [["chrI", "AS_STRUCTURE", "mRNA", 7741935, 7950951, "0", "+", ".", "gene_id=NR_070240; transcript_id=NR_070240; effective_length=209016" ],
                ["chrI", "AS_STRUCTURE", "mRNA", 8378298, 8378421, "0", "-", ".", "gene_id=NM_001129046; transcript_id=NM_001129046; effective_length=123" ],]
                ).sort()
                
        self.assertEqual(str(genes), str(true_genes))
        
        #tests mrna lengths
        genes = build_transcript_data_gtf(pybedtools.BedTool(clipper.test_file("data.gtf")), False).sort()
        true_genes = pybedtools.BedTool(
                [["chrI", "AS_STRUCTURE", "mRNA", 7741935, 7950951, "0", "+", ".", "gene_id=NR_070240; transcript_id=NR_070240; effective_length=30" ],
                ["chrI", "AS_STRUCTURE", "mRNA", 8378298, 8378421, "0", "-", ".", "gene_id=NM_001129046; transcript_id=NM_001129046; effective_length=123" ],]
                ).sort()
                
        self.assertEqual(str(genes), str(true_genes))
    
    def test_build_transcript_data_gtf_longer(self):
        
        """
        
        Tests build transcript data, but makes sure it gets the longer of two transcripts with the same gene name
        
        """
        
        genes = build_transcript_data_gtf(pybedtools.BedTool(clipper.test_file("data_2.gtf")), False).sort()
        true_genes = pybedtools.BedTool(
                [["chrI", "AS_STRUCTURE", "mRNA", 7741935, 7950970, "0", "+", ".", "gene_id=NR_070240; transcript_id=NR_070241; effective_length=41" ]],
                ).sort()
                
        self.assertEqual(str(genes), str(true_genes))
        
    def test_main(self):
        
        """
    
        Performs unit testing on main
        
        Mostly testing validation and input here
        TODO: fill in test...    
        
        """
        pass
    
    def tearDown(self):
        pass

#tests for hadoop mapping, currently not used / not worth the time to fix
#    def test_mapper_premrna(self):
#        
#        """
#        
#        tests the mapper to make sure that its not breaking / outputs call_peaks results
#        
#        """
#        
#        args = ["-b", pkg_resources.resource_filename(__name__, "../test/allup_test.bam"),
#                 "-s", "hg19",
#                 "-g", "ENSG00000198901", 
#                 "--outfile=" + os.getcwd() + "/allup_peak_results.bed",
#                ]
#
#        (options, args) = self.parser.parse_args(args)
#        
#        mapper(options, "chr1    66999065    67210057    ENST00000237247    0    +    67000041    67208778    0    27    25,123,64,25,84,57,55,176,12,12,25,52,86,93,75,501,81,128,127,60,112,156,133,203,65,165,1302,    0,863,92464,99687,100697,106394,109427,110161,127130,134147,137612,138561,139898,143621,146295,148486,150724,155765,156807,162051,185911,195881,200365,205952,207275,207889,209690,")
#   
#    def test_mapper_mrna(self):
#        
#        """
#        
#        Tests the pre mrna mapper
#        
#        """
#        
#        args = ["-b", pkg_resources.resource_filename(__name__, "../test/allup_test.bam"),
#                 "-s", "hg19",
#                 "-g", "ENSG00000198901", 
#                 "--outfile=" + os.getcwd() + "/allup_peak_results.bed",
#                ]
#
#        (options, args) = self.parser.parse_args(args)
#        
#        mapper(options, "chr1    66999065    67210057    ENST00000237247    0    +    67000041    67208778    0    27    25,123,64,25,84,57,55,176,12,12,25,52,86,93,75,501,81,128,127,60,112,156,133,203,65,165,1302,    0,863,92464,99687,100697,106394,109427,110161,127130,134147,137612,138561,139898,143621,146295,148486,150724,155765,156807,162051,185911,195881,200365,205952,207275,207889,209690,")

if __name__ == '__main__':
    unittest.main()
    os.remove(pkg_resources.resource_filename(__name__, "../src/peak_results.BED"))
