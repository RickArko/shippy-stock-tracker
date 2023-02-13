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

# Starter Workflow
1. Due to time constraints and machine and version contraints not everything will work out of the box in the api
1. Installed a separate conda env on a linux machine
1. Wrote  functions to extract a common financial dataframe for the examples provided
1. Assuming "Sources" always structure their reports the same the functions will work for any each ticker.
1. The parser can be easily extended to incorporate a new source.
1. Eventually I'd want to add more sources and build up a document database of financial pdfs, but this illustrates the basic idea.
1. Going to comment the financial endpoint since it doesn't currently work with fastapi, but it'd only take the time and motivation to make everything work, going to leave that as a future exercise

# Example Results 
See: (src\data\pdf-to-table.PNG)
![example-results](src\data\pdf-to-table.PNG)