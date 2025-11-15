#!/usr/bin/env python
# `test_Converter.py` by Wayne Decatur
# This is to run tests for `PubMed_Central_ID_Converter_for_humans`.
#**-------------------------------------------------------------------------**#
# this goes in 'tests'
import pytest
import os
import sys
from io import StringIO
import fnmatch
import glob
import filecmp
import urllib
import requests
import pandas as pd
import numpy as np
from pathlib import Path
import time

# Run this file while working directory is at root,
# like `pytest -v tests/test_Converter.py` 
# -or-
# if want printing from the pytests tests
# like `pytest -s -vv tests/test_Converter.py` 

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
PMC_id_convert_dataframe_output_prefix = 'PMC_id_convert_dataframe_output' # default Pandas dataframe file name prefix
 

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



def compare_files_content(file1_path, file2_path):
    '''
    Compare content ignoring whitespace differences
    '''
    data1 = read_and_process_file4content_check(file1_path)
    data2 = read_and_process_file4content_check(file2_path)

    assert len(data1) == len(data2), f"Files have different number of lines: {len(data1)} vs {len(data2)}"

    for i, (line1, line2) in enumerate(zip(data1, data2), 1):
        assert line1 == line2, f"Difference found at line {i}:\nFile 1: {' '.join(line1)}\nFile 2: {' '.join(line2)}"

    return True  # If we get here, the files are identical in content
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


# Check suqingdong's pmc-id-converter is getting same results as in the past
#--------------------------------------------------------------------------#
# Since I am relying on suqingdong's pmc-id-converter for comparison, I'm 
# checking the current version is working as expected before comparing any 
# results from my script.
def test_pmc_id_converter_cli_working_as_expected(tmp_path):
    the_old_result_text = '{"doi": "10.1007/s13205-018-1330-z", "pmcid": "PMC6039336", "pmid": 30003000, "requested-id": "30003000"}\n{"doi": "10.1002/open.201800095", "pmcid": "PMC6031859", "pmid": 30003001, "requested-id": "30003001"}\n{"doi": "10.1002/open.201800044", "pmcid": "PMC6031856", "pmid": 30003002, "requested-id": "30003002"}\n'
    current_result_fp = tmp_path / 'current_result.txt'
    os.system(f'pmc_idconv 30003000 30003001 30003002 > {current_result_fp}')
    assert current_result_fp.read_text() == the_old_result_text, "Result of `pmc_idconv 30003000 30003001 30003002 > current_result.json` is not matching expected." 

def test_pmc_id_converter_as_function_working_as_expected():
    original_stderr = sys.stderr
    sys.stderr = StringIO()  # Redirect stderr to a dummy buffer ;  this is 
    # because `PMC3531191123` is not a match and will produce `[2025-10-31 20:11:21 ID_CONV_API idconv ERROR MainThread:58] RecordError: Identifier not found in PMC for "PMC3531191123"`. The test will still give 'PASSED', but things will look bad. By shunting std.err to a dummy buffer, it avoids this passing through and making things look bad.
    the_old_result_dict = {'doi': '10.1093/nar/gks1195', 'pmcid': 'PMC3531190', 'pmid': 23193287, 'requested-id': 'PMC3531190'}
    the_old_query_result_list = ['23193287', None, '23193288']
    from pmc_id_converter import API
    current_example_result_a = API.idconv('PMC3531190')[0].data
    current_example_result_b = API.idconv('23193287')[0].data
    assert current_example_result_a == the_old_result_dict, "Result of `API.idconv('PMC3531190')[0].data` is not matching expected."
    assert current_example_result_b['doi'] == the_old_result_dict['doi'], (
        "Result of `API.idconv('23193287')[0].data` is not matching expected.")
    the_pmids = []
    query_ids = 'PMC3531190, PMC3531191123, PMC3531191'
    try: # see the `sys.stderr = StringIO()` line above
        records_of_query_results = API.idconv(query_ids)
        for record in records_of_query_results:
            the_pmids.append(record.data.get('pmid'))
        current_the_pmids = [str(x) if isinstance(x, int) else x for x in the_pmids] # otherwise they'll be integers which isn't what we really want as these are idenitifiers and not numbers to process in math
        assert current_the_pmids == the_old_query_result_list, (
            "Result of `API.idconv(query_ids)` is not matching expected.")
    finally:
            sys.stderr = original_stderr # Restore original stderr ; see 
            # the `sys.stderr = StringIO()` line above


# Check the `PubMed_Central_ID_Converter_for_humans` script is working as 
# expected 
#--------------------------------------------------------------------------#

# Have one test at least test fetching the data works in pyodide or Python using
# the current recommended 'service_root' URL, which is what will be used with
# Pyodide. (NOT SAME AS `pmc_id_converter` uses at this time.)
def test_can_get_data_from_service_root_API_whether_Pyodide_or_Python():
    # MAYBE IF CAN. BUT HOW TO RUN PYTEST SINCE NO COMMAND LINE!?!
    # Answer see https://pypi.org/project/pytest-pyodide/ under 
    #'run_in_pyodide' ====> Looks liken needs selenium or related things which I have used with MyBinder but I am trying to find examples where pyodide installed alongside tpyical ipykernel, too. SO MIGHT BE EASIER FOR NOW TO SKIP THIS TEST & TEST THAT PART DIRECTLY IN JUPYTERLITE MYSELF separate FOR NOW!!!!
    #...AND /OR...
    # maybe make a separate test file and use the following:
    '''
    import pytest
    # Run tests within a specific package
    pytest.main(['--pyargs', 'your_package.tests'])
    # You can also pass other pytest arguments
    # pytest.main(['--pyargs', 'your_package.tests', '-k', 'specific_test_name'])
    '''
    import sys

    if sys.platform == 'emscripten':  # found more commonly used on GitHub than `if "pyodide" in sys.modules`
        # Pyodide/JupyterLite specific code
        print(
            "[Running this test where pyodide is the underlying Python-basis.]")
        # Test can get data from PMC ID Converter API 
        # (https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/) using 
        # a Pyodide/JupyterLite-compatible approach
        # FOR NOW, just copy the pertinent code into a JupyterLite session.
        # (I HAVE YET TO MAKE THIS CODE BUT WHEN DO THAT, EITHER PASTE IN AS A 
        # DOCSTRING or OTHERWISE POINT FROM HERE TO THAT CODE.)
    else:
        # Normal Python code
        print(
            "[Running this test where typical Python is the underlying Python" \
            "-basis.]")
        # Test can get data from PMC ID Converter API
        # (https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/) with **current, 
        # suggested 'service_root' URL the 'standard' way. <=== NOTE USES SAME 
        # PLACE, I'll try with PYODIDE, WHICH IS NOT SAME AS `pmc_id_converter` 
        # uses at this time.
        service_root_url = (
            'https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/')
        res = requests.get(service_root_url, params={'ids': 'PMC3531190',
            'tool': 'my_tool',
            'email': 'my_email@example.com',
            'versions': 'no',
            'format': 'json',}).json()
        data = []
        for record in res['records']:
            if record.get('status') == 'error':
                errmsg = record['errmsg']
                _id = record.get('pmid') or record.get('pmcid') or record.get(
                    'doi')
                #context = Record(errmsg=errmsg, _id=_id)
            else:
                #context = Record(**record)
                context = record
            data += [context]
        assert 23193287 == data[0]['pmid'], (
            "The contact to the API with this `service_root_url` is not working as expected in Python.")





###-----------TESTING WORKS AS CLI-------------------------------------------###
# First check CLI ability of my script.
# -----------------------------------------------------------------------------#
pandas_df_expected = '''                         doi       pmcid      pmid requested-id
0  10.1007/s13205-018-1330-z  PMC6039336  30003000     30003000
1     10.1002/open.201800095  PMC6031859  30003001     30003001
2     10.1002/open.201800044  PMC6031856  30003002     30003002'''
csv_output_from_pandas_save_via_cli = '''doi,pmcid,pmid,requested-id
10.1007/s13205-018-1330-z,PMC6039336,30003000,30003000
10.1002/open.201800095,PMC6031859,30003001,30003001
10.1002/open.201800044,PMC6031856,30003002,30003002'''
def test_converter_cli_working_as_expected_for_Pandas(tmp_path):
    # Check makes pandas and result as expected by converting pmc_id_converter result to Pandas as I worked out in https://github.com/fomightez/pmc_id_converter_demo-binder
    from pmc_id_converter import API
    query_ids = '30003000 30003001 30003002'
    records_of_query_results = API.idconv(query_ids)
    records_of_query_results_data = [x.data for x in records_of_query_results] # make a list of the results dicts
    pmc_id_converter_df = pd.DataFrame.from_records(records_of_query_results_data)
    pmc_id_converter_df['pmid'] = pmc_id_converter_df['pmid'].apply(lambda x: str(int(x)) if pd.notna(x) else np.nan) # Don't want the pmid column values becoming floats/integer; however, do want the NaN staying that way & `Int64` helps with that
    #print(pmc_id_converter_df)
    #print(pandas_df_expected)
    assert pmc_id_converter_df.to_string() == pandas_df_expected, ("Result of using suqingdong's pmc_id_converter and then converting the result to a dataframe does not make the expected dataframe content.")
    time.sleep(0.3)
    # Now that established suqingdong's pmc_id_converter can be used to make an
    # expected dataframe, set up things to next check my script will make same.
    pmc_idconv_pandas_result_filepath = tmp_path / 'pmc_idconv_pandas_result.txt'
    with open(pmc_idconv_pandas_result_filepath, 'w') as f:
        f.write(pmc_id_converter_df.to_string())
    PMC_ID_Converter_for_humans_cli_result = tmp_path / 'PMC_ID_Converter_for_humans_cli_result.txt'
    os.system(f'PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform pandas 2>/dev/null > {PMC_ID_Converter_for_humans_cli_result}') # `2>/dev/null > output.txt` is so stderr feedback to user about saving files doesn't untidy the test
    assert PMC_ID_Converter_for_humans_cli_result.read_text().rstrip('\n') == pmc_idconv_pandas_result_filepath.read_text(), ("Result of using PMC_ID_Converter_for_humans on command line is not matching Pandas dataframe expected from `PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform pandas > pmc_idconv_cli_result.txt` equivalent.") # Note the extra `rstrip('\n')` there fixes the fact that the shell adds another newline when you use redirect to make a file.
    time.sleep(0.3)
    os.system(f'PMC_id_convert 30003000 30003001 30003002 --email test_settings 2>/dev/null > {PMC_ID_Converter_for_humans_cli_result}') # `2>/dev/null > output.txt` is so stderr feedback to user about saving files doesn't untidy the test
    assert PMC_ID_Converter_for_humans_cli_result.read_text().rstrip('\n') == pmc_idconv_pandas_result_filepath.read_text(), ("Result of using PMC_ID_Converter_for_humans on command line is not matching Pandas dataframe expected without `outform` being set as 'pandas'.") # Note the extra `rstrip('\n')` there fixes the fact that the shell adds another newline when you use redirect to make a file.
    # Read in the CSV and check content to verify the functionality of making the CSV
    assert Path(f"{PMC_id_convert_dataframe_output_prefix}.csv").read_text().rstrip('\n') == csv_output_from_pandas_save_via_cli, ("The expected CSV from the dataframe doesn't seem to be generated properly.") # Note the extra `rstrip('\n')` there fixes the fact that the shell adds another newline when you use redirect to make a file.
    # Read in converter result from saved pickled dataframe to verify the functionality of making the pickled dataframe
    df_newly_made_by_PMC_ID_Converter_for_humans = pd.read_pickle(f"{PMC_id_convert_dataframe_output_prefix}.pkl")
    assert df_newly_made_by_PMC_ID_Converter_for_humans.equals(pmc_id_converter_df), ("The expected pickled dataframe from the dataframe doesn't seem to be generated properly.")


expected_dictionary_result_text = '''[{'doi': '10.1007/s13205-018-1330-z', 'pmcid': 'PMC6039336', 'pmid': 30003000, 'requested-id': '30003000'}, {'doi': '10.1002/open.201800095', 'pmcid': 'PMC6031859', 'pmid': 30003001, 'requested-id': '30003001'}, {'doi': '10.1002/open.201800044', 'pmcid': 'PMC6031856', 'pmid': 30003002, 'requested-id': '30003002'}]'''
def test_converter_cli_working_as_expected_for_list_of_dictionaries(tmp_path):
    # Check you can make a dictionary and result same as pmc_id_converter
    # READ in PICKLED list of  DICTIONAries
    PMC_ID_Converter_for_humans_cli_result = tmp_path / 'PMC_ID_Converter_for_humans_cli_json_result.txt'
    time.sleep(0.3)
    os.system(f'PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform dictionaries > {PMC_ID_Converter_for_humans_cli_result}')
    assert PMC_ID_Converter_for_humans_cli_result.read_text().rstrip('\n') == expected_dictionary_result_text, ("Result of using PMC_ID_Converter_for_humans on command line is not matching list of dictionaries expected from `?????` equivalent.") # Note the extra `rstrip('\n')` there fixes the fact that the shell adds another newline when you use redirect to make a file.


# this first version of `expected_json_result_text` doesn't get used, see after it about docstring issue.
expected_json_result_text = '''[
  {"doi": "10.1007/s13205-018-1330-z", "pmcid": "PMC6039336", "pmid": 30003000, "requested-id": "30003000"},
  {"doi": "10.1002/open.201800095", "pmcid": "PMC6031859", "pmid": 30003001, "requested-id": "30003001"},
  {"doi": "10.1002/open.201800044", "pmcid": "PMC6031856", "pmid": 30003002, "requested-id": "30003002"}
]'''
# I was getting weird whitespace addded after commas on each line when defined `expected_json_result_text` with a docstring above!! This fixed it to now add spurious whitespace that shouldn't be there!
expected_json_result_text = (
    '[\n'
    '  {"doi": "10.1007/s13205-018-1330-z", "pmcid": "PMC6039336", "pmid": 30003000, "requested-id": "30003000"},\n'
    '  {"doi": "10.1002/open.201800095", "pmcid": "PMC6031859", "pmid": 30003001, "requested-id": "30003001"},\n'
    '  {"doi": "10.1002/open.201800044", "pmcid": "PMC6031856", "pmid": 30003002, "requested-id": "30003002"}\n'
    ']'
)
def test_converter_cli_working_as_expected_for_json(tmp_path):
    '''
    Online JSON Validation tool: https://jsonlint.com/
    '''
    # Check you can make json and result similar as if pmc_id_converter result converted to json
    #`pmc_idconv` does not actually make Valid JSON and so I will fix it so I can compare to 
    # result it produces. `pmc_idconv` should make good content, jut not the exact valid format, so
    # use the output to convert to Valid JSON and compare to that to check my 
    # new script.
    # NOTE THAT I DO THIS A MORE BRUTEFORCE STRING conversion route HERE, which I think is probably good as it will make more likely to catch errors that may come up in the `json` package that the script relies on for this conversion. So in a way, each will check the other & end up making things more robust because they are more orthologous than doing the conversion the same way.
    pmc_idconv_cli_result = tmp_path / 'pmc_idconv_cli_result.json'
    time.sleep(0.3)
    os.system(f'pmc_idconv 30003000 30003001 30003002 > {pmc_idconv_cli_result}')
    pmc_idconv_cli_result_as_VALID_json = pmc_idconv_cli_result.read_text().replace('}','},') # start converting to Valid JSON
    pmc_idconv_cli_result_as_VALID_json = pmc_idconv_cli_result_as_VALID_json.replace('{','  {') # convert to Valid JSON
    pmc_idconv_cli_result_as_VALID_json = f"[\n{pmc_idconv_cli_result_as_VALID_json[:-2]}\n]"
    #print(pmc_idconv_cli_result_as_VALID_json)
    assert pmc_idconv_cli_result_as_VALID_json == expected_json_result_text, ("Result of `pmc_idconv 30003000 30003001 30003002 > pmc_idconv_cli_result.json` equivalent not ending up being processed into valid JSON expected.")
    # Now that have made valid JSON using pmc_idconv, try my script & test by comparing result
    PMC_ID_Converter_for_humans_cli_result = tmp_path / 'PMC_ID_Converter_for_humans_cli_json_result.txt'
    time.sleep(0.3)
    os.system(f'PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform json > {PMC_ID_Converter_for_humans_cli_result}')
    assert PMC_ID_Converter_for_humans_cli_result.read_text().rstrip('\n') == pmc_idconv_cli_result_as_VALID_json, ("Result of using PMC_ID_Converter_for_humans on command line is not matching JSON-formatted text expected from `PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform json > pmc_idconv_cli_result.txt` equivalent.") # Note the extra `rstrip('\n')` there fixes the fact that the shell adds another newline when you use redirect to make a file.



expected_jsonl_result_text = (
    '{"doi": "10.1007/s13205-018-1330-z", "pmcid": "PMC6039336", "pmid": 30003000, "requested-id": "30003000"}\n'
    '{"doi": "10.1002/open.201800095", "pmcid": "PMC6031859", "pmid": 30003001, "requested-id": "30003001"}\n'
    '{"doi": "10.1002/open.201800044", "pmcid": "PMC6031856", "pmid": 30003002, "requested-id": "30003002"}\n'
)
def test_converter_cli_working_as_expected_for_JSONL(tmp_path):
    '''
    >"JSONL (JSON Lines) or NDJSON (Newline Delimited JSON), where each line is a separate, independent JSON object."
    See more about it at https://jsonlines.org/ where they even have a validator tool page.
    '''
    # Check you can make JSONL and result similar as if pmc_id_converter result? 
    #`pmc_idconv` does not actually make Valid JSON, it makes JSONL. `pmc_idconv` should make good content, so
    # use the output to make sure it is JSONL and compare to that to check my new script.
    pmc_idconv_cli_result = tmp_path / 'pmc_idconv_cli_result.txt'
    os.system(f'pmc_idconv 30003000 30003001 30003002 > {pmc_idconv_cli_result}')
    pmc_idconv_cli_result_as_jsonl = pmc_idconv_cli_result.read_text()
    assert pmc_idconv_cli_result_as_jsonl == expected_jsonl_result_text, ("Result of `pmc_idconv 30003000 30003001 30003002 > pmc_idconv_cli_result.txt` equivalent not generating JSONL expected.")
    # Now that have made JSONL using pmc_idconv, try my script & test by comparing result
    PMC_ID_Converter_for_humans_cli_result = tmp_path / 'PMC_ID_Converter_for_humans_cli_result.txt'
    time.sleep(0.3)
    os.system(f'PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform jsonl > {PMC_ID_Converter_for_humans_cli_result}')
    assert PMC_ID_Converter_for_humans_cli_result.read_text() == pmc_idconv_cli_result_as_jsonl, ("Result of using PMC_ID_Converter_for_humans on command line is not matching JSONL-formatted text (JSONL (JSON Lines) or NDJSON (Newline Delimited JSON)) expected from `PMC_id_convert 30003000 30003001 30003002 --email test_settings --outform jsonl > pmc_idconv_cli_result.txt` equivalent." )


def test_converter_cli_working_to_store_email_and_use_stored(tmp_path):
    # Initiate saving an email address and then check it worked by reading the
    # email to see if matched expected. Then test it can use the stored email
    # to do a query without needing email address.
    pmc_idconv_cli_result = tmp_path / 'pmc_idconv_cli_result.txt'
    time.sleep(0.3)
    os.system(f'PMC_id_convert 30003000 30003001 30003002 --email test_settings 2>/dev/null > {pmc_idconv_cli_result}') 
    config_file_filepath = Path.home() / '.pmc_id_converter' / 'config.json'
    assert config_file_filepath.read_text().rstrip('\n') == '{"email": "my_email@example.com"}', ("The email doesn't seem to get stored correctly when running from the command line.")
    pmc_idconv_cli_result_using_stored_email = tmp_path / 'pmc_idconv_cli_result_using_stored_email.txt'
    time.sleep(0.3)
    os.system(f'PMC_id_convert 30003000 30003001 30003002 2>/dev/null > {pmc_idconv_cli_result_using_stored_email}')
    assert pmc_idconv_cli_result_using_stored_email.read_text().rstrip('\n') == pandas_df_expected, ("The stored email doesn't seem to get used???!?!") # Note the extra `rstrip('\n')` there fixes the fact that the shell adds another newline when you use redirect to make a file.






###-----------TESTING WORKS AS FUNCTION--------------------------------------###
# Now check my script when used as a function
#(since the checks CLI works in ways expected was done with separate, thorough tests and the tests it works via functions paraellels it largely, the tests themselves will condensed into smaller groupings with the specific feedback providing details of one that may have failed)
def test_converter_function_working_as_expected():
    from PMC_ID_Converter_for_humans import PMC_id_convert
    # The check that it makes pandas dataframe and result as expected is done 
    # in next test, specifically
    # `test_converter_function_working_to_store_email_and_use_stored()`
    # That next test also inlcudes testing it makes pickled file of that 
    # dataframe. If that worked, I assume the CSV worked as well since that part 
    # already tested when code using on command line.
    
    # Check you can make a dictionary and result same as pmc_id_converter
    time.sleep(0.3)
    r = PMC_id_convert(
        '30003000 30003001 30003002', email = 'test_settings', 
        outform = 'dictionaries')
    assert isinstance(r, list)
    assert isinstance(r[0], dict)
    assert repr(r) == expected_dictionary_result_text, ("Result of using "
        "PMC_ID_Converter_for_humans as a function is not matching list of "
        "dictionaries expected from `PMC_id_convert('30003000 30003001 "
        "30003002', email = 'test_settings', outform = 'dictionaries')`." )
    

    # Check you can make json and result same as if pmc_id_converter result converted to json
    time.sleep(0.3)
    rj = PMC_id_convert(
        '30003000 30003001 30003002', email = 'test_settings', 
        outform = 'json')
    assert str(rj) == expected_json_result_text.rstrip('\n'), ("Result of "
        "using PMC_ID_Converter_for_humans as a function is not matching "
        "JSON-formatted text expected from `PMC_id_convert('30003000 "
        "30003001 30003002', email = 'test_settings', outform = 'json')`." )

    # Check can make jsonl result
    time.sleep(0.3)
    rjl = PMC_id_convert(
        '30003000 30003001 30003002', email = 'test_settings', 
        outform = 'jsonl')
    assert str(rjl) == expected_jsonl_result_text.rstrip('\n'), ("Result of "
        "using PMC_ID_Converter_for_humans as a function is not matching "
        "JSONL-formatted text (JSONL (JSON Lines) or NDJSON (Newline Delimited "
        "JSON)) expected from `PMC_id_convert('30003000 30003001 30003002', "
        "email = 'test_settings', outform = 'jsonl')`." )



def test_converter_function_working_to_store_email_and_use_stored(tmp_path):
    # Check can store and use email with function use
    # THIS ALSO TESTS MAKING A DATAFRAME WITH CORRECT CONTENT using the 
    # function. And that a pickled dataframe is also made. If that worked, I 
    # assume the CSV worked as well since that part already tested when code 
    # using on command line.
    from PMC_ID_Converter_for_humans import PMC_id_convert
    original_stderr = sys.stderr
    sys.stderr = StringIO()  # Redirect stderr to a dummy buffer ;  this is 
    # because `PMC3531191123` is not a match and will produce `[2025-10-31 20:11:21 ID_CONV_API idconv ERROR MainThread:58] RecordError: Identifier not found in PMC for "PMC3531191123"`. The test will still give 'PASSED', but things will look bad. By shunting std.err to a dummy buffer, it avoids this passing through and making things look bad.
    try:
        #delete any old pickled df result
        os.remove(f"{PMC_id_convert_dataframe_output_prefix}.pkl")
        time.sleep(0.3)
        r_df = PMC_id_convert(
            'PMC3531190 PMC3531191123 PMC3531191', email = 'test_settings')
        assert isinstance(r_df, pd.DataFrame)
        time.sleep(0.3)
        r_df2 = PMC_id_convert('PMC3531190 PMC3531191123 PMC3531191')
        assert isinstance(r_df2, pd.DataFrame)
        assert r_df.equals(r_df2), (
            "The returned dataframe doesn't seem to be generated properly.")
        # check pickled dataframe to make sure made something correct
        df_newly_made_by_PMC_ID_Converter_by_function = pd.read_pickle(f"{PMC_id_convert_dataframe_output_prefix}.pkl")
        assert df_newly_made_by_PMC_ID_Converter_by_function.equals(r_df), (
            "The expected pickled dataframe doesn't seem to be generated "
            "properly when the function utilized & no email provided.")
    finally:
            sys.stderr = original_stderr # Restore original stderr ; see 
            # the `sys.stderr = StringIO()` line above
