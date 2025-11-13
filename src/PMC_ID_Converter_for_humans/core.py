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
# Save this as `core_test.py` and run `%pip install requests pandas` in a cell and 
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
#
PMC_id_convert_dataframe_output_prefix = 'PMC_id_convert_dataframe_output' # default Pandas dataframe file name prefix
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
import re





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


def validate_email(email):
    """
    Basic email validation.
    Returns (is_valid, error_message)
    """
    if not email or email in ['None', 'NoneSetYet']:
        return False, "Email cannot be 'None' or empty"
    
    # Basic email pattern check
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return False, f"'{email}' does not appear to be a valid email address"
    
    return True, None
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
        email = 'my_email@example.com'
        save_email(email)
    elif email == 'NoneSetYet':
        # Try to load saved email
        email = load_email()
        if not email:
            raise ValueError(
                "No email provided and no saved email found. "
                "When calling `PMC_id_convert()` include setting email, like `PMC_id_convert(email='<email address here>')`"
                ". \n**EXITING !!**.\n"
            )
            sys.exit(1)
    else:
        # Validate email before saving
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            raise ValueError(
                f"Invalid email address provided: {error_msg}\n"
                f"Please provide a valid email address.\n"
                f"Example: PMC_id_convert(..., email='<email address here>')\n"
                "**EXITING !!**\n"
            )
        save_email(email)

    # Final validation check (for loaded emails too)
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        raise ValueError(
            f"Email validation failed: {error_msg}\n"
            f"Please update your email using: PMC_id_convert(..., email='<email address here>')\n"
            "**EXITING !!**\n"
        )



    '''
    if email == 'test_settings':
        email='my_email@example.com'
    elif email == 'NoneSetYet':
        # get email set
        raise SystemExit(
            "You need to set your email in the call the to command or in the "\
            "code used to call the function. \n**EXITING !!**.\n")
    '''
    


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
        try:
            res = requests.get(proxy_url)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"API request failed: {str(e)}\n"
                f"This may be due to:\n"
                f"  - Invalid email address: '{email}'\n"
                f"  - Network connectivity issues\n"
                f"  - NCBI API service problems\n"
                f"Please verify your email is valid and try again.\n"
            )
        
        # Check if we got HTML (error) instead of expected format
        if res.text.strip().startswith('<'):
            raise Exception(
                "API returned an error page instead of data.\n"
                f"Possible causes:\n"
                f"  - Invalid or rejected email address: '{email}'\n"
                f"  - Invalid ID format in: {ids}\n"
                f"  - API parameter issues\n"
                f"Please verify your inputs and try again."
            )
        
        try:
            json_response = res.json()
        except json.JSONDecodeError as e:
            raise Exception(
                f"Failed to parse API response as JSON: {str(e)}\n"
                f"Response received: {res.text[:200]}...\n"
                f"This often indicates the API rejected your request.\n"
                f"Check that email '{email}' is valid."
            )
        
        data = []
        for record in json_response.get('records', []):
            if record.get('status') == 'error':
                errmsg = record['errmsg']
                _id = record.get('pmid') or record.get('pmcid') or record.get('doi')
                context = record
            else:
                context = record
            data += [context]
        #return data # FOR TESTING/DEVELOPMENT, STOP HERE. OTHERWISE FORMAT OUTPUT!
    else:
        # Code that will work with typical versions of Python to communicate
        # with API.
        api_service_root_url = (
                'https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/')
        try:
            response = requests.get(api_service_root_url, params=params)
            response.raise_for_status()
            res = response.json()
        except requests.exceptions.HTTPError as e:
            raise Exception(
                f"HTTP error from NCBI API: {e}\n"
                f"Status code: {response.status_code}\n"
                f"This may indicate:\n"
                f"  - Invalid or rejected email: '{email}'\n"
                f"  - Too many requests (rate limiting)\n"
                f"  - API service issues\n"
            )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Network error while contacting NCBI API: {str(e)}\n"
                f"Please check your internet connection and try again.\n"
            )
        except json.JSONDecodeError as e:
            raise Exception(
                f"Failed to parse API response: {str(e)}\n"
                f"Response text: {response.text[:200]}...\n"
                f"The API likely rejected your request. Check your email: '{email}'\n"
            )
        
        data = []
        for record in res.get('records', []):
            if record.get('status') == 'error':
                errmsg = record['errmsg']
                _id = record.get('pmid') or record.get('pmcid') or record.get('doi')
                context = record
            else:
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
        csv_to_make_fn = '{}.csv'.format(
            PMC_id_convert_dataframe_output_prefix)
        pickled_df_to_make_fn = '{}.pkl'.format(
            PMC_id_convert_dataframe_output_prefix)
        df.to_csv(csv_to_make_fn,index = False)
        df.to_pickle(pickled_df_to_make_fn)
        # Let user know
        notify_of_csv_string = ("A dataframe of the data "
        "has been saved as a file in a manner where other "
        "software can access it (comma-separated form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'.".format(csv_to_make_fn))
        notify_pickled_df_string = ("A dataframe of the data "
        "has been saved as a file in a manner where other "
        "Python programs can access it (pickled form).\n"
        "RESULTING DATAFRAME is stored as ==> '{}'.".format(
            pickled_df_to_make_fn))
        sys.stderr.write(notify_of_csv_string + '\n')
        sys.stderr.write(notify_pickled_df_string + '\n')
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
    parser.add_argument('--email', default=None, help='Email address')
    parser.add_argument('--outform', 
                        choices=['pandas', 'json', 'jsonl', 'dictionaries'],
                        default='pandas',
                        help='Output Format (default: pandas)')
    args = parser.parse_args()

    # Determine email to use
    if args.email:
        email = args.email
        if email != 'test_settings':  # Don't save test settings
            # Validate email before trying to save
            is_valid, error_msg = validate_email(email)
            if not is_valid:
                raise ValueError(
                    f"Invalid email address provided: {error_msg}\n"
                    f"Please provide a valid email address.\n"
                    f"Example: PMC_id_convert --email <email address here> PMC3531190\n"
                    "**EXITING !!**\n"
                )
            save_email(email)
    else:
        email = load_email()
        if not email:
            print("Error: No email found. Please provide --email on first use.")
            #print("Example: %run core_test.py --email your@email.com PMC3531190")
            print("Example: PMC_id_convert --email <email address here> PMC3531190")
            print("-or")
            print("Example: %run core_test.py --email <email address here> PMC3531190")
            sys.exit(1)
    
    # Join the IDs with commas for the API
    ids_string = ','.join(args.ids)
    
    result = PMC_id_convert(ids_string, email=email, outform = args.outform)
    print(result)

if __name__ == "__main__":
    main()