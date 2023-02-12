# Financial Document Parsing
Need an automated way to extract varying length tables of financial details:

## Requirements
A working financial pdf parser will **extract all financial tables from .pdf to a pandas dataframe**

The parser should be able to handle the following: 
    - different units on ammounts (m, b, etc)
    - different ordering on columns
    - different number of years
    - time frequency (quarterly, monthly, etc.)


## Possible Workflow
    - image based vs. text based
        - image based will require some sort of `ocr` will not attempt to handle this yet
    
    - Text based pdf
        - camelot - well suited particularly for tabular data
        - non-trivial to install - hard conflicts with api libraries
            - Describe installation (#todo:)
                - install [ghostscript](https://ghostscript.com/releases/gsdnld.html)
                - install camelot

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