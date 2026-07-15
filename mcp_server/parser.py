import logging

import pandas as pd
from pydantic import ValidationError

from schema import Transaction
from utils import clean_date, infer_raw_category

logging.basicConfig(level=logging.INFO)


def parse_bank_csv(filepath: str):
    df = pd.read_csv(filepath)

    transactions = []

    for idx, row in df.iterrows():

        try:
            if pd.isna(row["amount"]):
                raise ValueError("missing amount")

            txn = Transaction(
                date=clean_date(str(row["date"])),
                description=str(row["description"]).strip(),
                amount=float(row["amount"]),
                raw_category=infer_raw_category(
                    str(row["description"])
                ),
            )

            transactions.append(txn)

        except Exception as e:
            logging.warning(
                f"Skipping row {idx}: {e}"
            )

    return transactions