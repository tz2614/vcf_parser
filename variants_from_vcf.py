#!usr/bin/python2

from __future__ import print_function
import sys
import os
import vcf


"""generate a list of variants from an annotated vcf against the transcripts in transcript_list"""

"""transcript_list = a python list of refseq IDs"""

def get_variants_in_vcf(annotated_vcf, transcript_list):

	""" Return a list of all variants in an annotated vcf which are annotated against the transcripts in transcript_list

	Args:
		vcf(str): an annotated vcf filepath
		transcript_list(list): a list of refseq transcripts
	Returns:
		list of pyvcf Record objects"""

	record_list = []

	assert type(transcript_list) == list, "{} is NOT a list".format(transcript_list)

	# open the annotated vcf and search records that contain the gene of interest, return the record as a pyvcf Record object

	rf_path = os.path.dirname(annotated_vcf)
	error_log = os.path.join(rf_path, "vcf_parse_error_log.txt")	

	with open (annotated_vcf, "r") as vcf_file:

		""" handle errors generated using a try, except statement and record the some of the common errors in error log, 
		if none generated then no log is recorded."""

		try: 
			vcf_reader = vcf.Reader(vcf_file)

		except (TypeError, RuntimeError, NameError, ValueError) as e:
			with open(error_log, "a") as err_log:
				err_log.writelines(e)


		"""Iterate through the INFO header and find the field containing RefSeq ID, e.g. "RefSeq", return the index as i."""

		with open (annotated_vcf, "r") as vcf_file:
			for line in vcf_file:
				if line.startswith("##INFO=<ID=CSQ"):
					fields = line.split(":")[-1].split("|")
					for index, field in enumerate(fields):
						if field == "RefSeq":
							i = index

		"""Then in the INFO "CSQ" field i, check if the RefSeq ID matches any RefSeq ID in the transcript list. 
		If there is a match and not already present, add it to the list; if the RefSeq ID field is empty record it in error log."""

		for record in vcf_reader:
			
			CSQ = record.INFO["CSQ"]

			for line in CSQ:
				info = line.split("|")[i]
			
				if info in transcript_list and record not in record_list:
					print (line)
					record_list.append(record)


				elif info == "":
					print ("RefSeq not found")
					with open (error_log) as err_log:
						err_log,writelines("RefSeq not found in {}".format(line))
						continue
				else:
					continue

	return  (record_list)

def main(annotated_vcf, gene2transcript_manifest):

	# check that the manifest exist as a data source for the transcript_list
	assert os.path.exists(annotated_vcf), "{} DO NOT exists".format(annotated_vcf)
	assert os.path.exists(gene2transcript_manifest), "{} DO NOT exist".format(gene2transcript_manifest)

	# generate a list of transcripts using RefSeq IDs from gene2transcript_manifest)
	transcript_list = []

	with open(gene2transcript_manifest, "r") as gene_transcripts:
		for line in gene_transcripts:
			fields = line.strip().split("\t")
			transcript_list.append(fields[-1])

	# create a list of vcf variants in the form of pyvcf objects
	record_list = get_variants_in_vcf(annotated_vcf, transcript_list)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2])








