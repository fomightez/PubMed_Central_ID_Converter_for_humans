#!/usr/bin/env python
# PMC_ID_Converter_for_humans by Wayne Decatur
# ver 0.1.0
#
#*******************************************************************************
# 
#
#
#
#
#
# Dependencies beyond the mostly standard libraries/modules:
# ????
#
#

#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# sheperds_all_list_combinations_thru_find_overlap_in_list.py list1.txt list2.txt list3.txt list4.txt list5.txt
#-----------------------------------
#
# To use via Python:
# from PMC_ID_Converter_for_humans import PMC_id_convert
# PMC_id_convert()
#
#*******************************************************************************
#


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
##
# ?
#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************





















#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###

import sys
import os
import argparse





'''
Use:
from PMC_ID_Converter_for_humans import PMC_id_convert
PMC_id_convert()
'''

expected_jsonl_result_text = (
    '{"doi": "10.1007/s13205-018-1330-z", "pmcid": "PMC6039336", "pmid": 30003000, "requested-id": "30003000"}\n'
    '{"doi": "10.1002/open.201800095", "pmcid": "PMC6031859", "pmid": 30003001, "requested-id": "30003001"}\n'
    '{"doi": "10.1002/open.201800044", "pmcid": "PMC6031856", "pmid": 30003002, "requested-id": "30003002"}\n'
)
 input_text_filepath = sys.argv[1]
 def PMC_id_convert():
    print(expected_jsonl_result_text)