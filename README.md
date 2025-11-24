# PubMed_Central_ID_Converter_for_humans

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PubMed_Central_ID_Converter_for_humans/main?urlpath=%2Flab%2Ftree%2Fdemo.ipynb)


*tl;dr:*  
Click any `launch binder` badge on this page to get started learning about this package with demonstrations inside your browser.

----------------

### PubMed_Central_ID_Converter_for_humans: PubMed API use for humans

A simple library for using the PubMed Central ID Convert API for dealing biomedical and scientific literature in modern Python/Jupyter ecosystems.  

Summary of Key Features:
- **Control format of results: Python dictionary, Pandas dataframe, or JSON/JSONL text**.
- **It is Pyodide/JupyterLite compatible**. (WASM-based Python compatible!)  

**Features**

A Python-based library for using the PubMed Central ID Convert API for dealing biomedical and scientific literature in modern Python/Jupyter ecosystems.  
Use the library to get PubMed Central identifiers, PubMed identifiers (PMIDs), and DOI identifiers for scientific literature.  
In an opionated choice, the default format for the results is a Pandas dataframe; however, this can be adjusted via flag/argument settings. If you aren't familiar with Pandas, the provided demonstration notebook illustrates convenient steps, such using the Pandas dataframe to make a lookup table / key-value mapping.  
It is largely kernel agnostic as far as Python goes, which means you can use it in JupyterLite as well as in more standard Jupyter where a typical ipykernel is involved. At present, command line use of the library is not compatible with Pyodide/JupyterLite. Command line use is fully allowed in a typical system with a POSIX system shell (Bash/zsh-type) where standard Python is installed.    
Set your email address once and use the tool subsequently without supplying it each time. (Email address is needed by NCBI in efforts to help insure you play nice with API use.)   

**Limitations**

Keep in mind according to [the PMC ID Converter API](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/), the basis for this package's coverting identifiers functionality:  
>"The PMC ID Converter API will only return related IDs if the article is in PubMed Central (PMC)."

This means the PubMed_Central_ID_Converter_for_humans won't return identifiers for those articles not present in PubMed Central.

(Note that [nelsonaloysio's package `pubmed-id`](https://pypi.org/project/pubmed-id/) discussed under the 'Influences' section below, goes beyond using the API and can do some webscaping, supposedly, and so it is able to return identifiers for those not present in PubMed Central, see [here](https://github.com/nelsonaloysio/pubmed-id#scrape-data-from-website) about , "Note: some papers are unavailable from the API, but still return data when scraped, e.g., PMID 15356126". Therefore, [nelsonaloysio's package `pubmed-id`](https://pypi.org/project/pubmed-id/) is able to return identifiers for those not present in PubMed Central)


-------

## Installation

### Using uv (recommended)
```bash
uv add ????
```

### Using pip
```bash
pip install git+https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git
```

### From source (developers)
```bash
git clone https://github.com/fomightez/PubMed_Central_ID_Converter_for_humans.git
cd PubMed_Central_ID_Converter_for_humans
uv pip install -e .
```

## Try it without installing

`<MyBinder session instructions go here>` TBF

## Try it in JupyterLite

I would suggest using the package with a full ipykernel as JupyterLite/WASM-based Python are still relatively new & experimental; however, this package will work in present JupyterLite, as you `<CAN POSSIBLY TRY HERE AT GITHUB REPO TO BE MADE IN FUTURE>`? (TBD if add this....) 

## Quick Start

You should see the demo notebook for a thorough introduction.   
Below is the Quick Start Guide to get you started with the two main routes to use the package.  
Note although only the first example under each category includes setting the email address, you have to do this step at least once after installation, no matter what type of query you are executing. The email address will be stored and so you only need to supply the address once. (Each new MyBinder-served session counts as a new installation and so you have to do that step each session.)

### Command Line Tools

```bash
# Display Usage
PMC_id_convert --help


# PMID
PMC_id_convert 30003000 --email <your_email_here>
# PMCID
PMC_id_convert PMC6039336
# DOI
PMC_id_convert 10.1007/s13205-018-1330-z
# Multiple IDs
PMC_id_convert 30003000 30003001 30003002
# Output to a file named with a custom predfix
PMC_id_convert 30003000 30003001 30003002 -out_prefix results_from_my_ids
# Output as list of dictionaries
PMC_id_convert 30003000 30003001 30003002 --outform dictionaries

# Output Dataframe to string that can be redirected

# Output list of dictionaries to text that can be redirected
PMC_id_convert 30003000 30003001 30003002 --outform dictionaries --return_string

# Output as JSON text (can be redirected to file if, desired)
PMC_id_convert 30003000 30003001 30003002 --outform json

# Output as JSONL (JSON Lines), a.k.a. NDJSON (Newline Delimited JSON) text (can be redirected to file, if desired)
PMC_id_convert 30003000 30003001 30003002 --outform jsonl
```

### Python API

```python
from src.PMC_ID_Converter_for_humans import PMC_id_convert

# PMCID
PMC_id_convert('PMC3531190', email = '<your_email_here>')

# Multiple IDs
PMC_id_convert('PMC3531190', 'PMC3531191123', 'PMC3531191')

# PMID
PMC_id_convert('23193287')

# DOI
PMC_id_convert('10.1093/nar/gks1195')

# Output to a file named with a custom predfix

# Output as list of dictionaries

# Output as JSON

# Output as JSONL
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
