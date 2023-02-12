### PDF PARSE


    # TEXT.find("Income")
    
    # min(TEXT.find("Income"), TEXT.find("Sales"))
    # TEXT.find("Sales", "revenue")
    # INCOME_START = TEXT.find("Income(Gross)")
    # REVENUE_START = TEXT.find("Revenue")
    # GROSS_START = TEXT.find("Gross")
    # EBITDA_START = TEXT.find("EBITDA")
    # TAX_START = TEXT.find("Income")
    
    # financial_dict = {
    #     "income": INCOME_START,
    #     "revenue": REVENUE_START,
    #     "gross": GROSS_START,
    #     "tax": TAX_START,
    # }
    # sorted([INCOME_START, REVENUE_START, GROSS_START, EBITDA_START, TAX_START])
    
    
    # [
    #     {"ticker": "AAPL",
    #         “year”: “2022”
    #             "financials": {
    #                 "revenue": 394330000000,
    #                 "gross_income": 170780000000,
    #                 "ebitda": 130540000000,
    #                 "income_tax": 14530000000
    #             }
    #         }, {
    #             "ticker": "AAPL",
    #             “year”: “2021”,
    #             "financials": {
    #                 "revenue": 365820000000,
    #                 "gross_income": 152840000000,
    #                 "ebitda": 120230000000,
    #                 "income_tax": 9680000000
    #             }
    #         }]


YEARS = (2018, 2019, 2020, 2021, 2022)

PRETAX_INCOME = TEXT[TEXT.find("Pretax"):TEXT.find("Sales")].split("\n")

amts = [f for f in PRETAX_INCOME if "B" in f]
list(zip(YEARS, amts))



####
# def parse_financials(ticker: str, source: str) -> pd.DataFrame:
#     ticker = ticker.upper()
#     source = source.title()

#     data_dir = Path("src").joinpath("data")
#     pdfs = list(data_dir.glob("*.pdf"))

#     matching_financials = [
#         f
#         for f in pdfs
#         if (ticker in f.name) and (source in f.name)
#     ]

#     if len(matching_financials) == 0:
#         # TODO: Retreive from elsewhere
#         raise ValueError(f"No financials found for {ticker} from {source}")
#     matching_financials = matching_financials[0]

#     reader = PdfReader(fname)
#     number_of_pages = len(reader.pages)
#     page = reader.pages[0]
#     text = page.extract_text()

#     return pd.DataFrame()

# # Mock request
# request = {"ticker": "AAPL", "source": "Morning Star"}
# matching_financials = [
#     f
#     for f in PDFS
#     if request["ticker"].upper() in f.name and request["source"] in f.name
# ]
# fname = matching_financials[0]

# fname = PDFS[0]
# fname.name.split("Document")

# reader = PdfReader(fname)
# number_of_pages = len(reader.pages)
# page = reader.pages[0]
# text = page.extract_text()

# print(text)
