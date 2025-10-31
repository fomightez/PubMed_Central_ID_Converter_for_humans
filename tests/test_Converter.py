#!/usr/bin/env python
# `test_Converter.py` by Wayne Decatur
# This is to run tests for `PubMed_Central_ID_Converter_for_humans`.
#**-------------------------------------------------------------------------**#
# this goes in same folder with ????????????????????
# `my_conftest_for_test_missing_residue_detailer.py` & `conftest.py` that will 
# be for  testing `missing_residue_detailer.py`, which needs to be in root 
import pytest
import os
import fnmatch
import glob
import filecmp
from bs4 import BeautifulSoup

# Run this file while working directory is at root,
# like `pytest -v tests/test_PubMed_Central_ID_Converter_for_humans.py` 
# -or-
# if want printing from the pytests tests
# like `pytest -s -v tests/test_PubMed_Central_ID_Converter_for_humans.py` 

# Compares the results of my `PubMed_Central_ID_Converter_for_humans.py` to the 
# results from pmc-id-converter (https://pypi.org/project/pmc-id-converter/) as
# well as reformatted versions of those results to test of makes Pandas 
# dataframes.
# First, testa that pmc-id-converter is still producing same results since I am
# relying on that for comparison.



#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
aMMMMMMMM_prefix = "????????_" # Used here?????
 

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************



#*******************************************************************************
##################################
#  FILE PATHS       #

##################################
#

current_provided_exampleMMMMMMM = "???????????????" # USED HERE??????
 
#
#*******************************************************************************
#*****************************END FILE PATHS************************************







###---------------------------HELPER FUNCTIONS-------------------------------###


def write_string_to_file(s, fn):
    '''
    Takes a string, `s`, and a name for a file & writes the string to the file.
    '''
    with open(fn, 'w') as output_file:
        output_file.write(s)




def compare_file_content_equality(file1_path, file2_path, msg="Files are not identical in content, ignoring whitespace differences."):
    '''
    Compare two files content ignoring whitespace differences

    Has a default assertion message, but you can pass your own string as third
    argument in call or only pass the two paths and use the default.
    '''
    assert compare_files_content(file1_path, file2_path), msg



###-------------------------END OF HELPER FUNCTIONS--------------------------###
###-------------------------END OF HELPER FUNCTIONS--------------------------###








###----------------------------------TESTS-----------------------------------###
###----------------------------------TESTS-----------------------------------###


# Check the pmc-id-converter is getting same results as it did in the past
#--------------------------------------------------------------------------#
# Since I am relying on ththe pmc-id-converter for comparison, I'm checking 
# the current version is working as expected.
def test_pmc_id_converter_working_as_expected():
    the_old_result_dict = {'doi': '10.1093/nar/gks1195', 'pmcid': 'PMC3531190', 'pmid': 23193287, 'requested-id': 'PMC3531190'}
    the_old_query_result_list = ['23193287', None, '23193288']
    from pmc_id_converter import API
    example_result_a = API.idconv('PMC3531190')[0].data
    example_results_b = API.idconv('23193287')[0].data
    assert example_result_a == the_old_result_dict, "Result of `API.idconv('PMC3531190')[0].data` is not matching expected."
    assert example_result_b == the_old_result_dict, "Result of `API.idconv('23193287')[0].data` is not matching expected."
    the_pmids = []
    query_ids = 'PMC3531190, PMC3531191123, PMC3531191'
    records_of_query_results = API.idconv(query_ids)
    for record in records_of_query_results:
        the_pmids.append(record.data.get('pmid'))
    the_pmids = [str(x) if isinstance(x, int) else x for x in the_pmids] # otherwise they'll be integers which isn't what we really want as these are idenitifiers and not numbers to process in math
    assert the_pmids == the_old_query_result_list, "Result of `API.idconv(query_ids)` is not matching expected."



'''
# This next test tests that a file with the proper name convention can be 
# supplied as souce of input data instead of fetching PDB file header from 
# Protein Data Bank
def test_file_can_be_used_as_source(dir_2_put_test_files):  # Add the fixtures as parameters
    # I added later the ability to supply a file as the source the header. This 
    # should test that as it uses a PDB id code that does not exist and so the 
    # only way it will run to work and produce anything is if it uses the file
    # I supplied as source of header. (It cannot fall back to fetching & using 
    # something from Protein Data Bank.) Since using content corresponding to 
    # 1d66, output should look like what I expect for 1d66 output, which is 
    # among the PDB id codes tested below, and so testing the content making 
    # part of the script will get handled there but this will at least test 
    # there is output file as expected if used file as input. In other words, as 
    # written the test for prioritizing reading a file just makes sure output 
    # of some sort made by script.
    PDB_code_for_file_read_test = "4tSt" # "4tst is a useful PDB id for a non-existing structure"-https://proteopedia.org/wiki/index.php/Believe_It_or_Not#Notes & 
    # https://proteopedia.org/wiki/index.php/4tst
    suffix_4_results = "_missing_residue_details.html" # Has to match what 
    # `missing_residue_detailer.py` has for this.
    file_input_suffix = "_header4missing.txt" # Has to match what 
    # `missing_residue_detailer.py` has for this.
    file_used_as_input = PDB_code_for_file_read_test + file_input_suffix
    output_expected = PDB_code_for_file_read_test.lower() + suffix_4_results
    assert os.path.isfile(TEST_FILES_DIR + output_expected), \
        f"The expected file ouput {dir_2_put_test_files + output_expected} made using {file_used_as_input} as input does not exist"
    # the file used as input should also now be in the test files and have 1d66
    # header as content. Next assert test it at least the file is there.
    assert os.path.isfile(TEST_FILES_DIR + file_used_as_input), \
        f"The file {file_used_as_input} does not seem to have been moved back to the test location?"
    # FUTURE IMPROVEMENT: add when script more mature to see if content in `output_expected` matches HTML made by script for 1d66?


# Get & Iterate on each pair and check if the text without HTML matches. Because
# if that fails, surely the more detailed HTML will fail.
def get_text_pairs_and_ids(directory):
    # Print what files we find to debug
    print(f"Looking in directory: {os.path.abspath(directory)}")
    fgij_files = glob.glob(os.path.join(directory, "fgij_text_*.txt"))
    print(f"Found fgij files: {fgij_files}")
    
    pairs_and_ids = []
    for fgij_file in fgij_files:
        # Extract ID from filename
        id_part = os.path.basename(fgij_file).split('_')[-1].split('.')[0]
        # Find matching fmrd file
        fmrd_file = os.path.join(directory, f"fmrd_text_{id_part}.txt")
        print(f"Looking for matching file: {fmrd_file}")
        if os.path.exists(fmrd_file):
            pairs_and_ids.append(((os.path.basename(fgij_file), 
                                 os.path.basename(fmrd_file)), 
                                id_part))
    return pairs_and_ids


# Get pairs and IDs from the correct directory
#test_dir = "additional_nbs/tests" # I had hoped to avoid having this in multiple places, so let's see if this works: (IT does and so I don't know why cannot use those not fixtures to pass things. Maybe only fixtures allowed in tests?)
from my_conftest_for_test_missing_residue_detailer import TEST_FILES_DIR
test_dir = TEST_FILES_DIR
pairs_and_ids = get_text_pairs_and_ids(test_dir)
pairs, ids = zip(*pairs_and_ids)


def generate_test_name(val):
    """Generates a custom test ID for each test case.
    Args:
        int: interger for index position.
    Returns:
        A string representing the custom test ID.
    """
    return f"From {ids[val]}"

#@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=ids) # works to give PDB id code in brackets for end of name of function but I wanted to customize a bit further & so see next line
@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=generate_test_name)

def test_text_files_match(pair_index, dir_2_put_test_files):
    """Test that each pair of text files have identical content."""
    file1, file2 = pairs[pair_index]
    assert filecmp.cmp(dir_2_put_test_files + file1, dir_2_put_test_files + file2, shallow=False), \
        f"Files {dir_2_put_test_files + file1} and {dir_2_put_test_files + file2} do not have identical content"
'''
# THIS EARLIER FORM WORKS BUT...
# Note that it appears it cannot be simpler because I am using 
# `text_pairs_to_process` from `conftest.py` and so cannot use in `@pytest.mark.parametrize()` direct because not yet define. This gets around that.
#BUT DOESN'T REALLY WORK With `ids` to name the tests  by the PDB id and if I use something like `request.node.name = f"test_text_files_match[{ids[pair_index]}]"` in the test, I am still hard coding in number and order with `"pair_index", [0, 1]`. SO THIS 
# IS FINE FOR TESTING SET UP INITIALLY BUT WILL LIMIT ME AS I HOPE TO ADD MORE
# details from more PDB diles to test.
'''
@pytest.mark.parametrize("pair_index", [0, 1])
def test_text_files_match(text_pairs_to_process, pair_index, dir_2_put_test_files):
    """Test that each pair of text files have identical content."""
    file1, file2 = text_pairs_to_process[pair_index]
    assert filecmp.cmp(dir_2_put_test_files + file1, dir_2_put_test_files + file2, shallow=False), \
        f"Files {dir_2_put_test_files + file1} and {dir_2_put_test_files + file2} do not have identical content"
'''




'''
# Now up the level to checking if the HTML matches. Get & Iterate on each pair .
def get_html_pairs_and_ids(directory):
    # Print what files we find to debug
    print(f"Looking in directory: {os.path.abspath(directory)}")
    fgij_files = glob.glob(os.path.join(directory, "fgij_html_*.html"))
    print(f"Found fgij files: {fgij_files}")
    
    pairs_and_ids = []
    for fgij_file in fgij_files:
        # Extract ID from filename
        id_part = os.path.basename(fgij_file).split('_')[-1].split('.')[0]
        # Find matching fmrd file
        fmrd_file = os.path.join(directory, f"fmrd_html_{id_part}.html")
        print(f"Looking for matching file: {fmrd_file}")
        if os.path.exists(fmrd_file):
            pairs_and_ids.append(((os.path.basename(fgij_file), 
                                 os.path.basename(fmrd_file)), 
                                id_part))
    return pairs_and_ids

# Get pairs and IDs from the correct directory
hpairs_and_ids = get_html_pairs_and_ids(test_dir)
hpairs, hids = zip(*hpairs_and_ids)

#@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=hids) # works to give PDB id code in brackets for end of name of function but I wanted to customize a bit further & so see next line
@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=generate_test_name)
def test_html_files_match(pair_index, dir_2_put_test_files):
    """Test that each pair of text files have identical content."""
    file1, file2 = pairs[pair_index]
    assert filecmp.cmp(dir_2_put_test_files + file1, dir_2_put_test_files + file2, shallow=False), \
        f"Files {dir_2_put_test_files + file1} and {dir_2_put_test_files + file2} do not have identical content"
'''