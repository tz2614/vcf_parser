# CBI-5 DOPS
- variants_from_vcf.py

By Tengyue Zheng
25/09/2018

## User Requirements

*Create a script to parse a large text file and output a small specified subset of data.*
Return a list of all variants in an annotated vcf, which are annotated against the transcript in transcript_list

## dependencies

os, sys and vcf module imported from python standard library
pytest module for unit testing installed using pip
e.g. activate the virtualenv

```Python
$source env/bin/activate

$pip install -U pytest
```

## Function Description

Parse a vcf file and get a list of pyvcf Record object containing the annotated variants of transcripts from the transcript list using vcf python module.

## Instructions

To use the function from my script, parse the following as arguments to my function

1. first argument: path to the annotated vcf

e.g. /mnt/storage/home/garnerm/vcf_fix/X006200.refseq_nirvana_203.fixed.annotated.vcf 

Note: This vcf has modified to conform with the latest vcf specifications, if your vcf do not conform to the vcf specification then running the script will likely have relevant errors displayed and recorded in the vcf_parse_error_log.txt.

2. second argument: a list of transcripts or RefSeq IDs

This should be derived from your function, or alternatively if you have access to the cluster at CUH lab you can use
/mnt/storage/data/NGS/nirvana_genes2transcripts

3. To test the function, first navigate to the directory where the test script is stored

```Bash
cd /mnt/storage/home/zhengt/Competencies/CBI-5_Programming/DOPs/
```

then execute the pytest installed
	
```Python
$pytest test_variants_from_vcf.py
```

If the test passes, then a green double dash line with the message "1 passed in ###### second" should be displayd.

4. To execute the program and get a list of pyvcf Record objects from the vcf file, type the following
e.g. assume the path to the vcf file = PATH2VCF

```Bash
$python variant_from_vcf.py PATH2VCF /mnt/storage/data/NGS/nirvana_gene2transcript
```

Note: If you have a list of RefSeq transcripts already within your script, then simply use the path to vcf and your list of transcripts as arguments to my function to get a list of objects, without running the script from command line. To do this import the function from myscript into your python as a python module such as 

```Python
from variant_from_vcf import get_variants_in_vcf
```

then invoke the function in your script
e.g.
list of transcript = REFSEQ_IDS
the path to the vcf file = PATH2VCF

```Python
get_variants_in_vcf(PATH2VCF, REFSEQ_IDS)
```

If you have any queries or require any support information on the script and function, please email tengyue.zheng@nhs.net
