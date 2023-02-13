from pathlib import Path

import pandas as pd


def find_local_pdf(ticker: str, source: str) -> Path:
    """Find local pdf for ticker and source.

    Raises:
        ValueError: No matching financials for ticker source

    Returns:
        Path: path to local pdf
    """
    ticker = ticker.upper()
    source = source.lower()

    data_dir = Path("src").joinpath("data")
    pdfs = list(data_dir.glob("*.pdf"))

    matching_financials = [f for f in pdfs if (ticker in f.name) and (source in f.name.lower())]

    if len(matching_financials) == 0:
        # TODO: Retreive from elsewhere
        raise ValueError(f"No financials found for {ticker} from {source}")

    return matching_financials[0]


def parse_pdf_text(fname: Path) -> str:
    """Parse pdf into dataframe.

    Args:
        fname (Path): path to pdf

    Returns:
        pd.DataFrame: dataframe of parsed pdf
    """
    from PyPDF2 import PdfReader

    reader = PdfReader(fname)
    number_of_pages = len(reader.pages)
    page = reader.pages[0]
    text = page.extract_text()
    return text


def get_financials(TEXT: str, header: str = "Financials"):
    """Extract financials from text as string."""
    start = TEXT.find(header)
    return TEXT[start:]


if __name__ == "__main__":
    ticker = "AAPL"
    source = "Morning Star"
    source = "jpm"
    pdfpath = find_local_pdf(ticker, source)
    TEXT = parse_pdf_text(pdfpath)

    # YEARS = (2018, 2019, 2020, 2021, 2022)

    # for y in YEARS:
    #     result = TEXT.find(str(y))

    # print(get_financials(TEXT, "Financials"))

    # BODY = get_financials(TEXT, "Financials")
    # BODY[]
