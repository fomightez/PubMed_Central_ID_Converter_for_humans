# PubMed_Central_ID_Converter_for_humans

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PubMed_Central_ID_Converter_for_humans/main?urlpath=%2Flab%2Ftree%2Fdemo.ipynb)


*tl;dr:*  
Click any `launch binder` badge on this page to get started learning about this package with demonstrations inside your browser.

----------------

### PubMed_Central_ID_Converter_for_humans: PubMed API use for humans

A simple library for using the PubMed Central ID Convert API for biomedical and scientific literature in modern Python/Jupyter ecosystems.  

Summary of Key Features:
- **Control format of results: Python dictionary, Pandas dataframe, or JSON/JSONL text**.
- **It is Pyodide/JupyterLite compatible**. (WASM-based Python compatible!)  

**Features**

A Python-based library for using the PubMed Central ID Convert API for biomedical and scientific literature in modern Python/Jupyter ecosystems.  
Use the library to get PubMed Central identifiers, PubMed identifiers (PMIDs), and DOI identifiers for scientific literature.  
In an opionated choice, the default format for the results is a Pandas dataframe; however, this can be adjusted via flag/argument settings. If you aren't familiar with Pandas, the provided demonstration notebook illustrates convenient steps, such using the Pandas dataframe to make a lookup table / key-value mapping.  
It is largely kernel-agnostic as far as Python goes, which means you can use it in JupyterLite as well as in more standard Jupyter where a typical ipykernel is involved. At present, command line use of the library is not compatible with Pyodide/JupyterLite. Command line use is fully allowed in a typical system with a POSIX system shell (Bash/zsh-type) where standard Python is installed.    
Set your email address once and use the tool subsequently without supplying it each time. (Email address is needed by NCBI in efforts to help insure you play nice with API use.)   

**Limitations**

Keep in mind according to [the PMC ID Converter API](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/), the basis for this package's coverting identifiers functionality:  
>"The PMC ID Converter API will only return related IDs if the article is in PubMed Central (PMC)."

This means the PubMed_Central_ID_Converter_for_humans won't return identifiers for those articles not present in PubMed Central.

(Note that [nelsonaloysio's package `pubmed-id`](https://pypi.org/project/pubmed-id/) discussed under the 'Influences' section below, goes beyond using the API and can do some webscaping, supposedly, and so it is able to return identifiers for those not present in PubMed Central, see [here](https://github.com/nelsonaloysio/pubmed-id#scrape-data-from-website) about , "Note: some papers are unavailable from the API, but still return data when scraped, e.g., PMID 15356126". Therefore, [nelsonaloysio's package `pubmed-id`](https://pypi.org/project/pubmed-id/) is able to return identifiers for those not present in PubMed Central)


-------

Here's three ways to try the package without installing anything on your machine; the first two you run it via your browser and the final one is for `uv` users:

## Try it without touching your system

Try the package in an active Jupyter session without installing anything or logging in or signing up for anything via remote virtual sessions provided by the MyBinder service.
`<MyBinder session instructions go here>` TBD

If you end up making anything useful, be sure to download it to your local maching as the sessions are ephemeral on remote virtual machine with which you are anonymously connected.

JupyterLab interface: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PubMed_Central_ID_Converter_for_humans/main?urlpath=%2Flab%2Ftree%2Fdemo.ipynb)  
Jupyter Notebook 7+:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PubMed_Central_ID_Converter_for_humans/main?urlpath=%2Ftree%2Fdemo.ipynb)

## Try it in JupyterLite

I would suggest using the package with a full ipykernel as JupyterLite/WASM-based Python are still relatively new & experimental; however, this package will work in present JupyterLite with a Python-based kernel, as you can demonstrate in your JupyterLite session on your machine by pressing this following link:

[Open the JupyterLite demo notebook via litegitpuller](https://litegitpuller.readthedocs.io/en/latest/lite/lab/?branch=main&repo=https%3A%2F%2Fgithub.com%2Ffomightez%2FPubMed_Central_ID_Converter_for_humans&urlpath=notebooks%2Fjupyterlite_demo.ipynb)

JupyterLite has the advantage that everything stays on your own machine. If you have privacy or security concerns in relation to something in your workflow.

litegitpuller gets the entire package repo and offers the demo notebook. Alternatively, you could install the package in your JupyterLite session of choice by running `%pip install git+https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git PMC_id_convert` at the top of the notebook, and then you can run `from src.PMC_ID_Converter_for_humans import PMC_id_convert` to import the main function.



## `uv` users: Try it without installing permanently

If you want to test `PMC_id_convert` on the command line without actually installing it, you can directly run it yourself with the help of uv using `uvx`, like so:

```text
uvx --from git+https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git PMC_id_convert 30003000 --email <your_email_here>
```

## Installation

### Using `uv` (recommended)
```bash
uv add ????
```

You can also use `uv pip install ???` if you are using other `pip` workflows with `uv`.

### Using `pip`
```bash
pip install git+https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git
```

### From source (developers)
```bash
git clone https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git
cd PubMed_Central_ID_Converter_for_humans
uv pip install -e .
```



## Quick Start

You should see the demonstration notebook for a thorough introduction. Get the full, interactive experience of the demo notebook via MyBinder-served sessions, see under ['Try it without touching your system'](#try-it-without-touching-your-system). (Or [go here](https://nbviewer.org/github/fomightez/PubMed_Central_ID_Converter_for_humans/blob/main/demo.ipynb) for a dull, static version.)   
Below is the Quick Start Guide to get you started with the two main routes to use the package.  
Note although only the first example under each category includes setting the email address, you have to do this step at least once after installation, no matter what type of query you are executing. The email address will be stored, and so you only need to supply the address once. (Each new MyBinder-served session counts as a new installation and so you have to do that step each session.)

### Command Line Tool

Examples using the command line:

```bash
# Display Usage
PMC_id_convert --help


# PMID
PMC_id_convert 30003000 --email <your_email_here>

# PMCID
PMC_id_convert PMC6039336

# DOI (try quotes if this fails, see next example)
PMC_id_convert 10.1007/s13205-018-1330-z

# multiple DOIs (for improved chances it will work on most platforms, I suggest wrapping each DOI in quotes)
PMC_id_convert "10.1007/s13205-018-1330-z" "10.1093/nar/gks1195"

# Multiple IDs
PMC_id_convert 30003000 30003001 30003002

# Output data to a dataframe with the file named with a custom prefix
PMC_id_convert 30003000 30003001 30003002 -out_prefix results_from_my_ids

# Output data as a list of dictionaries to a Python pickle file (binary format)
PMC_id_convert 30003000 30003001 30003002 --outform dictionaries

# Output data as a Dataframe to text string that can be redirected
PMC_id_convert 30003000 30003001 30003002 --return_string

# Output data as a Dataframe to text string that can be redirected (same as above but explicit)
PMC_id_convert 30003000 30003001 30003002 --outform pandas --return_string

# Output data as a list of dictionaries to text that can be redirected
PMC_id_convert 30003000 30003001 30003002 --outform dictionaries --return_string

# Output data as JSON text
PMC_id_convert 30003000 30003001 30003002 --outform json

# Output data as JSONL (JSON Lines), a.k.a. NDJSON (Newline Delimited JSON), text
PMC_id_convert 30003000 30003001 30003002 --outform jsonl

# Output data as JSON text & redirect that to a file
PMC_id_convert 30003000 30003001 30003002 --outform json > output.txt

# Output data as JSONL (JSON Lines), a.k.a. NDJSON (Newline Delimited JSON), text  & redirect that to a file
PMC_id_convert 30003000 30003001 30003002 --outform jsonl > output.txt
```

### Python API 

Examples using the main function via Python:

```python
from src.PMC_ID_Converter_for_humans import PMC_id_convert

# PMCID
PMC_id_convert('PMC3531190', email = '<your_email_here>')

# Multiple IDs
PMC_id_convert('PMC3531190, PMC3531191123, PMC3531191')

# PMID
PMC_id_convert('23193287')

# DOI
PMC_id_convert('10.1093/nar/gks1195')

# multiple DOIs
PMC_id_convert('10.1093/nar/gks1195,10.1007/s13205-018-1330-z')

# Output data as a dataframe with dataframe displayed as well (will render in nice style in Jupyter)
PMC_id_convert('PMC3531190,PMC3531191123,PMC3531191', return_df = True)

# Output data as a dataframe and force a string representation to display, even in Jupyter
print(PMC_id_convert('PMC3531190,PMC3531191123,PMC3531191', return_df = True))

# Output data as a dataframe with the file named with a custom prefix  
PMC_id_convert('PMC3531190,PMC3531191123,PMC3531191', output_prefix = 'custom_file_name_suffix')

# Python list as input
python_list_ids = ['PMC3531190','PMC3531191123','PMC3531191']
id_list_as_text = ','.join(python_list_ids)
PMC_id_convert(id_list_as_text, output_prefix = 'shows_can_use_list')

# Output data as list of dictionaries
list_of_result_dicts = PMC_id_convert('PMC3531190, PMC3531191', outform = 'dictionaries')

# Output data as a JSON text string
print(PMC_id_convert('PMC3531190, PMC3531191', outform = 'json'))

# Output data as a JSONL (JSON Lines) text string
print(PMC_id_convert('PMC3531190, PMC3531191', outform = 'jsonl'))

# Output data as JSON text & redirect that to a file when running in IPython/Jupyter
result = PMC_id_convert('PMC3531190, PMC3531191', outform = 'json')
%store result >output.txt

# Output data as JSONL (JSON Lines) text  & redirect that to a file when running in IPython/Jupyter
result = PMC_id_convert('PMC3531190, PMC3531191', outform = 'jsonl')
%store result >output.txt

# Output data as JSON text & redirect that to a file when running in standard Python
result = PMC_id_convert('PMC3531190, PMC3531191', outform='json')
with open('output.txt', 'w') as f:
    f.write(result)

# Output data as JSONL (JSON Lines) text  & redirect that to a file when running in standard Python
result = PMC_id_convert('PMC3531190, PMC3531191', outform='jsonl')
with open('output.txt', 'w') as f:
    f.write(result)
```

---------


#### Influences & this package's place in the Python/Jupyter ecosystem <br>
<details>
  <summary>✚ <b><i>Details</i></b> (Click to see details)</summary>
  <p>Largely influenced by these two packages developed by others:</p>
  <ul>
    <li><a href="https://pypi.org/project/pmc-id-converter/">suqingdong's pmc-id-converter</a> (I have a demo offering for this package <a href="https://github.com/fomightez/pmc_id_converter_demo-binder">here</a> that you can run in your browser via the MyBinder service without touching your own system or logging into anything.)</li>
    <li><a href="https://pypi.org/project/pubmed-id/">nelsonaloysio's pubmed-id</a></li>
  </ul>
</details>




-----------



JupyterLab interface: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PubMed_Central_ID_Converter_for_humans/main?urlpath=%2Flab%2Ftree%2Fdemo.ipynb)  
Jupyter Notebook 7+:  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PubMed_Central_ID_Converter_for_humans/main?urlpath=%2Ftree%2Fdemo.ipynb)
