#!/usr/bin/env python
# PMC_ID_Converter_for_humans by Wayne Decatur
__version__ = '0.1.0'
#
#*******************************************************************************
# PubMed_Central_ID_Converter_for_humans: PubMed API use for humans
# A simple library for using the PubMed Central ID Convert API for dealing 
# biomedical and scientific literature in modern Python/Jupyter ecosystems.  
# Summary of Key Features:
# - Control format of results: Python dictionary, Pandas dataframe, or JSON/
#   JSONL text.
# - It is Pyodide/JupyterLite compatible. (WASM-based Python compatible!)
##Features##
#A Python-based library for using the PubMed Central ID Convert API for dealing 
# biomedical and scientific literature in modern Python/Jupyter ecosystems.  
# Use the library to get PubMed Central identifiers, PubMed identifiers (PMIDs), 
# and DOI identifiers for scientific literature.  
# In an opionated choice, the default format for the results is a Pandas 
# dataframe; however, this can be adjusted via flag/argument settings.  
# It is largely kernel agnostic as far as Python goes, which means you can use 
# it in JupyterLite as well as in more standard Jupyter where a typical 
# ipykernel is involved. At present, command line use of the library is not 
# compatible with Pyodide/JupyterLite. Command line use is fully allowed in a 
# typical system with a POSIX system shell (Bash/zsh-type) where standard Python 
# is installed.   
#
#
# Dependencies beyond the mostly standard libraries/modules:
# uv
# pandas
# 
# 
# 
# To do:
# - add to https://github.com/fomightez/pmc_id_converter_demo-binder pointing users at better resource!
# - remove showing you can get away with `--email test_settings` from 'CURRENT JUPYTERLITE TEST' because want to push users to use email.
# - change command lines to have `'<your_email_here>'` in all more standard command line
# examples, but somewhere else note how I tested in terminal while developping early, which current examples show!
# - I plan to add other arguments like `format` so expand early examples and 
# future ones to include maybe some of those, too.
#
#
# TO RUN:
# Example,
# Enter on the command line of your terminal, the line
#-----------------------------------
# uv run python -c "from PMC_ID_Converter_for_humans import PMC_id_convert; print(PMC_id_convert('PMC3531190', email='test_settings'))" > testing_better.txt
#-----------------------------------
# -or-
# uv pip install -e .     # LATER THIS WILL BE `pip install PMC-ID-Converter-for-humans` for general users
# PMC_id_convert PMC3531190 --email test@example.com > testing_better_still.txt
# -OR-
# PMC_id_convert PMC3531190 PMC3531191 --email test_settings > testing_multiples.txt
#
#
# To use via Python:
# from PMC_ID_Converter_for_humans import PMC_id_convert
# PMC_id_convert('PMC3531190', email = '<your_email_here>')
# 
#
#
# CURRENT JUPYTERLITE TEST along the the line command line use -- closest possible there:
# Save this as `core_test.py` and run `%pip install requests` in a cell and 
# then in a new cell run the following command:
# `%run core_test.py PMC3531190 --email test_settings`
# -or to show works with multiple ids:
# `%run core_test --email test_settings PMC3531190 PMC3531191`
# -OR- 
# `%run core_test PMC3531190 PMC3531191 --email test_settings`
# COMPARE THE RESULTS OF THOSE TO RUNNING `PMC_id_convert PMC3531190 --email test@example.com` and `PMC_id_convert PMC3531190 PMC3531191 --email test_settings`, respectively
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
from pathlib import Path
import argparse
import requests
import json





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
# This `if len(sys.argv) > 1:` and next line was also for when testing early 
# form, along with `print(expected_jsonl_result_text[:-1])` below
#if len(sys.argv) > 1:
#    input_text_filepath = sys.argv[1]






###---------------------------HELPER FUNCTIONS-------------------------------###



###------------------HELPER FUNCTIONS TO HANDLE STORING EMAIL----------------###
def get_config_file():
    """Get path to config file in user's home directory"""
    config_dir = Path.home() / '.pmc_id_converter'
    config_dir.mkdir(exist_ok=True)
    return config_dir / 'config.json'

def load_email():
    """Load saved email from config file"""
    config_file = get_config_file()
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('email')
    return None

def save_email(email):
    """Save email to config file"""
    config_file = get_config_file()
    with open(config_file, 'w') as f:
        json.dump({'email': email}, f)
###----------END OF HELPER FUNCTIONS TO HANDLE STORING EMAIL-----------------###


###--------------------------END OF HELPER FUNCTIONS-------------------------###
###--------------------------END OF HELPER FUNCTIONS-------------------------###












#*******************************************************************************
###------------------------'main' function of script-------------------------###


def PMC_id_convert(ids, email = 'NoneSetYet', outform = 'pandas'):
    tool='PMC_ID_Converter_for_humans'
    versions='no'
    # print(expected_jsonl_result_text[:-1]) # was adding one too many newlines, 
    # so leaving off the last character, makes it match expected # ONLY USED IN 
    # VERY EARLY DEVELOPMENT BEFORE ADDED CONNECTING TO API (also used with `len(sys.argv) > 1:` above)
    # LATER FOLLOW-UP. I think I know issue. Often when you redirect output to a file with `>` many systems add a newline. Later for pytest I was using things like `assert PMC_ID_Converter_for_humans_cli_result.read_text().rstrip('\n')`. Maybe `.rstrip('\n')` coukd have been useful here. 

    if email == 'test_settings':
        email='my_email@example.com'
    elif email == 'NoneSetYet':
        # get email set
        raise SystemExit(
            "You need to set your email in the call the to command or in the "\
            "code used to call the function. \n**EXITING !!**.\n")
    params={'ids': ids,
        'tool': tool,
        'email': email,
        'versions': versions,
        'format': 'json',}



    # Found this `if sys.platform == 'emscripten'` way of checking if running in 
    # WASM / pyodide situation by searching GitHub for 'pyodide'. Examples:
    # - https://github.com/mrirecon/bart
    # - https://github.com/twardoch/jiter-pupy 
    # - https://github.com/pygame-web/archives
    # Then looking around more I found that is the first suggestion in the 
    # Pyodide documentation at 
    # https://pyodide.org/en/latest/usage/faq.html#how-to-detect-that-code-is-run-with-pyodide -- "At run time, you
    # can check if Python is built with Emscripten (which is the case for 
    # Pyodide)"
    if sys.platform == 'emscripten':
        # Code that will work in Pyodide/JupyterLite situations to communicate 
        # with the API where things not as simple in late 2025.
        
        using_pyodide = True
        from urllib.parse import quote

        return_format = params['format']
        # Build the API URL with all required parameters
        api_url = f'https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids={ids}&format={return_format}&tool={tool}&email={email}'
        
        # Use CORS proxy
        proxy_url = f'https://api.allorigins.win/raw?url={quote(api_url, safe="")}'
        
        #print(f"Requesting: {api_url}")
        
        # Make request with requests package
        res = requests.get(proxy_url)
        res.raise_for_status()
        
        # Check if we got HTML (error) instead of expected format
        if res.text.strip().startswith('<'):
            raise Exception("API returned HTML instead of expected format. Check your parameters.")
        
        data = []
        for record in res.json()['records']:
            if record.get('status') == 'error':
                errmsg = record['errmsg']
                _id = record.get('pmid') or record.get('pmcid') or record.get(
                    'doi')
                #context = Record(errmsg=errmsg, _id=_id)
            else:
                #context = Record(**record) # I don't want to complicate with a class
                context = record
            data += [context]
        #return data # FOR TESTING/DEVELOPMENT, STOP HERE. OTHERWISE FORMAT OUTPUT!
    else:
        # Code that will work with typical versions of Python to communicate
        # with API.
        api_service_root_url = (
                'https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/')
        res = requests.get(api_service_root_url, params=params).json()
        data = []
        for record in res['records']:
            if record.get('status') == 'error':
                errmsg = record['errmsg']
                _id = record.get('pmid') or record.get('pmcid') or record.get(
                    'doi')
                #context = Record(errmsg=errmsg, _id=_id)
            else:
                #context = Record(**record) # I don't want to complicate with a class
                context = record
            data += [context]
        #return data # FOR TESTING/DEVELOPMENT, STOP HERE. OTHERWISE FORMAT OUTPUT!
    # Pandas as default
    if outform == 'jsonl':
        # this form is supposed to be good for streaming and for some reason is 
        # the default for output from suqingdong's pmc_id_converter (pmc_idconv 
        # on command line) at https://github.com/suqingdong/pmc_id_converter 
        '''
        >"JSONL (JSON Lines) or NDJSON (Newline Delimited JSON), where each line is a separate, independent JSON object."
        See more about it at https://jsonlines.org/ where they even have a validator tool page.
        '''
        #converted_jsonl = '\n'.join(data)
        #converted_jsonl = '\n'.join([str(d) for d in data])
        converted_jsonl = '\n'.join([json.dumps(d) for d in data])
        return converted_jsonl
    elif outform == 'json':
        # Make actual valid JSON from the list of dictionaries returned by API
        '''
        Online JSON Validation tool: https://jsonlint.com/
        '''
        #converted_json = json.dumps(data, indent=2) # want JSON with 2 spaces 
        # for indentation # THIS ORIGINAL ATTEMOPT GAVE VALID JSON BUT WITH each
        # key pair on a separate line and I want them all on one line to save 
        # files from getting super long when many identifiers used in query.S 
        # Format each object as a single line with space after commas
        json_lines = [json.dumps(item, separators=(', ', ': ')) for item in data]
        # Combine into an array with proper indentation
        converted_json = '[\n  ' + ',\n  '.join(json_lines) + '\n]'
        return converted_json
    elif outform == 'dictionaries':
        # Make a list of Python dictionaries and save in pickle/serialized form
        # to be read back in to Python.
        # No conversion actually needed here because this is the basic form the 
        # API returns -- a list of dictionaries with each dictionary 
        # corresponding to the individual queries
        return data
    else:
        # Make a Pandas dataframe
        import pandas as pd
        import numpy as np
        #records_of_query_results = API.idconv(query_ids)
        #records_of_query_results_data = [x.data for x in data] # make a list of the results dicts
        df = pd.DataFrame.from_records(data)
        df['pmid'] = df['pmid'].apply(
            lambda x: str(int(x)) if pd.notna(x) else np.nan) # Don't want the 
        # pmid column values becoming floats/integer; however, do want the NaN 
        # staying that way & `Int64` helps with that.
        df.reset_index(drop=True) # if any removed, need to reset the index
        df.to_csv('test_out.csv',index = False)
        df.to_pickle('test_out.pkl')
        # Let user know
        df_save_as_name = 'output_as_pandas' 
        notify_of_csv_string = ("A dataframe of the data "
        "has been saved as a file in a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}.csv'".format(df_save_as_name ))
        notify_pickling_string = ("A dataframe of the data "
        "has been saved as a file in a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'.pkl".format(df_save_as_name ))
    #return data
    return df
#*******************************************************************************
###-**********************END MAIN FUNCTION OF SCRIPT***********************-###
#*******************************************************************************










def main():
    import argparse

    ''' DON'T ACTUALLY NEED THIS HERE BECAUSE `nargs` USE FOR IDS HANDLING will cause it to print usage if none added but if want to customize handling can put this back.
    # Check if no arguments provided & print usage if now
    if len(sys.argv) == 1:
        parser = argparse.ArgumentParser()
        parser.print_help()
        sys.exit(1)
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('ids', nargs='+', help='One or more IDs to convert (space-separated)')
    parser.add_argument('--email', default='NoneSetYet', help='Email address')
    parser.add_argument('--outform', 
                        choices=['pandas', 'json', 'jsonl', 'dictionaries'],
                        default='pandas',
                        help='Output Format (default: pandas)')
    args = parser.parse_args()

    # Determine email to use
    if args.email:
        email = args.email
        if email != 'test_settings':  # Don't save test settings
            save_email(email)
    else:
        email = load_email()
        if not email:
            print("Error: No email found. Please provide --email on first use.")
            print("Example: %run core_test.py --email your@email.com PMC3531190")
            sys.exit(1)
    
    # Join the IDs with commas for the API
    ids_string = ','.join(args.ids)
    
    result = PMC_id_convert(ids_string, email=args.email, outform = args.outform)
    print(result)

if __name__ == "__main__":
    main()