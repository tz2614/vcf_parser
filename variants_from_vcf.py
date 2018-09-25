#!usr/bin/python

from __future__ import print_function
import sys
import os
import vcf
import pprint as pp


"""generate a list of variants from an annotated vcf against the transcripts in transcript_list"""

"""transcript_list = a python list of refseq IDs"""

def get_variants_in_vcf(annotated_vcf, transcript_list):

	""" Return a list of all variants in an annotated vcf which are annotated against the transcripts in transcript_list

	Args:
		vcf(str): an annotated vcf filepath
		transcript_list(list): a list of refseq transcripts
	Returns:
		list of pyvcf Record objects"""

	#gene2transcript = {}
	#genes = []
	#transcripts = []
	record_list = []

	#assert os.path.exists(transcript_list), "gene2transcript list DO NOT exists"
	assert os.path.exists(annotated_vcf), "{} DO NOT exists".format(annotated_vcf)
	assert type(transcript_list), "{} is NOT a list".format(transcript_list)

	# open the annotated vcf and search records that contain the gene of interest, return the record as a pyvcf Record object

	rf_path = os.path.dirname(annotated_vcf)
	error_log = os.path.join(rf_path, "vcf_parse_error_log.txt")	

	with open (annotated_vcf, "r") as vcf_file:

		""" handle errors generated using a try, except statement and record the some of the common errors in error log, 
		if none generated then no log is recorded."""

		try: 
			vcf_reader = vcf.Reader(vcf_file)

		except (TypeError, RuntimeError, NameError, ValueError):
			with open(error_log, "a") as err_log:
				err_log.writelines(TypeError)
				err_log.writelines(NameError)
				err_log.writelines(ValueError)
			pass


		for record in vcf_reader:
			
			CSQ = record.INFO["CSQ"]

			for line in CSQ:
				#print (line)
				infos = line.split("|")
				for info in infos:
					if info != "" and info in transcript_list and record not in record_list:
						#print (record.CHROM, record.POS, record.REF, record.ALT, CSQ)
						print (record)
						record_list.append(record)
					else:
						continue

			

	#pp.pprint (gene2transcript)
	#print ("Here is a list of pyvcf Record objects: \n")
	#print (record_list)
	return  (record_list)

def main(annotated_vcf, gene2transcript_manifest):

	# check that the manifest exist as a data source for the transcript_list
	assert os.path.exists(gene2transcript_manifest), "{} DO NOT exist".format(gene2transcript_manifest)

	transcript_list = []

	with open(gene2transcript_manifest, "r") as gene_transcripts:
		for line in gene_transcripts:
			fields = line.strip().split("\t")
			transcript_list.append(fields[-1])

	record_list = get_variants_in_vcf(annotated_vcf, transcript_list)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])








