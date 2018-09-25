import vcf
import sys

with open (sys.argv[1], "r") as vcf_file:
	vcf_reader = vcf.Reader(vcf_file)
	for record in vcf_reader:
		print record.POS