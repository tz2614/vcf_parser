#!usr/bin/python

import sys
import os

def remove_symbols_from_vcf(annotated_vcf):

	assert os.path.exists(annotated_vcf), "{} do not exists".format(annotated_vcf)

	with open (annotated_vcf) as vcf_file:
		for line in vcf_file:
			if line.startswith("##"):
				continue

			elif line.endswith(">"):
				continue

			else:
				print (line)
				fields = line.strip().split("|")
				for field in fields:
					if " " in field:
						print (field)
						fields.remove(field)
					elif "(" or ")" in field:
						print (field)
						fields.remove(field)
					else:
						continue

	return annotated_vcf

def main(annotated_vcf):

	remove_symbols_from_vcf(annotated_vcf)

if __name__ == "__main__":
	main(sys.argv[1])




