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
In an opionated choice, the default format for the results is a Pandas dataframe; however, this can be adjusted via flag/argument settings. The provided demonstration notebook illustrates using the Pandas dataframe to make a lookup table / key-value mapping.  
It is largely kernel agnostic as far as Python goes, which means you can use it in JupyterLite as well as in more standard Jupyter where a typical ipykernel is involved. At present, command line use of the library is not compatible with Pyodide/JupyterLite. Command line use is fully allowed in a typical system with a POSIX system shell (Bash/zsh-type) where standard Python is installed.    
Set your email address once and use the tool subsequently without supplying it each time. (Email address is needed by NCBI in efforts to help insure you play nice with API use.)   

**Limitations**

Keep in mind according to [the PMC ID Converter API](https://pmc.ncbi.nlm.nih.gov/tools/id-converter-api/), the basis for this package's coverting identifiers functionality:  
>"The PMC ID Converter API will only return related IDs if the article is in PubMed Central (PMC)."

This means the PubMed_Central_ID_Converter_for_humans won't return identifiers for those articles not present in PubMed Central.

(Note that [nelsonaloysio's package `pubmed-id`](https://pypi.org/project/pubmed-id/) discussed under the 'Influences' section below, goes beyond using the API and can do some webscaping, supposedly, and so it is able to return identifiers for those not present in PubMed Central, see [here](https://github.com/nelsonaloysio/pubmed-id#scrape-data-from-website) about , "Note: some papers are unavailable from the API, but still return data when scraped, e.g., PMID 15356126". Therefore, [nelsonaloysio's package `pubmed-id`](https://pypi.org/project/pubmed-id/) is able to return identifiers for those not present in PubMed Central)

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
