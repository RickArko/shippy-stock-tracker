from pathlib import Path
from typing import Dict, Union

import camelot
import pandas as pd
from src.parse_financials import find_local_pdf


def set_first_row_columns(df) -> pd.DataFrame:
    """Set first row as column names then drop."""
    df.columns = df.iloc[0]
    df = df.iloc[1:, :]
    return df


def parse_morningstar(path: Union[Path, str]):
    l = camelot.read_pdf(path, flavor="lattice")
    df = l[0].df
    df.columns = df.iloc[0]
    df = df.iloc[1:, :]
    df = df.set_index("")
    return df


def parse_jpm(path: Union[Path, str]):
    l = camelot.read_pdf(path, flavor="lattice", line_scale=100)
    r = []
    for i, table in enumerate(l):
        df = table.df
        df = set_first_row_columns(df)
        df = df.head(1)
        df = df.rename(columns={"": "type"})
        df.index = [i]
        df = df.loc[:, ~df.columns.duplicated()]  # remove duplicate cols
        df = df.set_index("type")
        df.index.name = None
        r.append(df)

    dffinancials = pd.concat(r)
    return dffinancials
    return df


def parse_financials(source: str, path: Union[Path, str]):
    """Parse all financial tables from pdf source and return dataframe."""
    availble_sources = ("Morning Star", "JPM")
    if source not in availble_sources:
        raise ValueError(f"Source must be one of {availble_sources}")

    source_map = {
        "Morning Star": parse_morningstar,
        "JPM": parse_jpm,
    }
    dffinancials = source_map.get(source)(path)
    return dffinancials


def summarise_financials(df: pd.DataFrame) -> Dict:
    """Create a nested dictionary of financials summary by year."""
    summary_dict = {}
    for year in df.columns:
        year_dict = {}
        year_dict["financials"] = {}
        for category in df.index:
            year_dict["financials"][category] = df.loc[category, year]
        summary_dict[year] = year_dict
    return summary_dict
