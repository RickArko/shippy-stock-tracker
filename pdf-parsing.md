# Financial Document Parsing
Need an automated way to extract varying length tables of financial details:

____
## Requirements
A working financial pdf parser will **extract all financial tables from .pdf to a pandas dataframe**

The parser should be able to handle the following: 
    - different units on ammounts (m, b, etc)
    - different ordering on columns
    - different number of years
    - time frequency (quarterly, monthly, etc.)


## Possible Workflow
  - Determine if image or text pdf
      - image based will require some sort of `ocr` will not attempt to handle this yet
  
  - For a text based pdf plan to use [camelot](https://camelot-py.readthedocs.io/en/master/)
      - designed particularly for tabular data
      - non-trivial to install - hard conflicts with api libraries
          - Describe installation (#todo:)
              - install [ghostscript](https://ghostscript.com/releases/gsdnld.html)
              - install [camelot](https://camelot-py.readthedocs.io/en/master/user/install.html#pip)
      - there are a lot of different options to configure camelot that will require a large # of pdfs to fine-tune optimal parameters
          - which parser `Lattice` or `Stream`
              - Lattice looks for lines on a page to identify a table
              - Stream looks for whitespaces between words

Pseduo-code:

```
    # for given ticker/source - look for local pdf
    ticker = "AAPL"
    source = "Morning Star"

    import camelot
    pdfpath = find_local_pdf(ticker, source)

    pdf = camelot.read_pdf(pdfpath) # return list of tables found

    results = []
    for table in pdf:
       df = table.df  # extract dataframe
       sum = summarise_financials(df)
       results.append(sum)

    dfsummary = pd.conact(results, ignore_index=True)
```