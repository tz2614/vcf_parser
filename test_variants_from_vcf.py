#!usr/bin/python

import pytest
import vcf
import variants_from_vcf
import shutil
import os

"""test that the get_variants_in_vcf function parses the vcf and returns the objects containing the correct information with regard to each variant"""

"""e.g T|401934|RNF223|NM_001205252.1||missense_variant|725|242|P/H||tolerated(0.22)|possibly_damaging(0.895)|NM_001205252.1:c.725C>A,
which has the following in the fixed fields
CHROM	POS     ID				REF     ALT
1       1007203 rs4633229       A       G
1       1007222 rs71628928      G       T"""


@pytest.fixture(scope="function")
def path_to_vcf():

	"""
    Set up and tear down test directory containing the annotated vcf
    """

	annotated_vcf = "/mnt/storage/home/garnerm/vcf_fix/X006200.refseq_nirvana_203.fixed.annotated.vcf"
	current_directory = os.getcwd()
	test_directory = os.path.abspath(os.path.join(current_directory, "test_runfolder"))

	# if the directory already exist then error
	assert not os.path.exists(test_directory), "The test directory {} already exists".format(test_directory)
	# create the directory
	os.makedirs(test_directory)
	
	rf_path = os.path.abspath(test_directory)

	"""
    make a copy of the vcf in the test_runfolder directory, and return the filepath to the vcf
	"""
	vcf_path = os.path.join(rf_path, "X006200.refseq_nirvana_203.fixed.annotated.vcf")
	shutil.copyfile(annotated_vcf, vcf_path)

	yield vcf_path

	# This runs after the test function is complete to clean up
	# It deletes the test directory we created and anything it contains
	shutil.rmtree(test_directory)

@pytest.fixture(scope="function")
def transcript_list():

	"""create test transcript_list"""

	transcript_list = ["NM_001205252.1"]

	return transcript_list

@pytest.mark.usefixtures("path_to_vcf")
def test_get_variants_in_vcf(path_to_vcf, transcript_list):

	"""take arguments from path_to_vcf and transcript_list and get a output frp, get_variants_in_vcf function,
	then check each object from the output, and see if values returned from the properties of each object is equal to the fixed field values as expected"""

	pyvcf_variants = variants_from_vcf.get_variants_in_vcf(path_to_vcf, transcript_list)

	for record in pyvcf_variants:

		print (record.CHROM)
		print (record.POS)
		print (record.REF)
		print (record.ALT)

		assert int(record.CHROM) == 1, "CHROM number of variant in list INCORRECT"
		assert int(record.POS) == 1007203 or int(record.POS) == 1007222, "POS of variant in list INCORRECT"
		assert str(record.REF) == "A" or str(record.REF) == "G", "REF of variant in list INCORRECT"
		assert str(record.ALT[0]) == "G" or str(record.ALT[0]) == "T", "ALT of variant in list INCORRECT"

	return record
