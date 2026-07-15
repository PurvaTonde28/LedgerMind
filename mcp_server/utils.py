from dateutil import parser


def clean_date(date_str: str) -> str:
    """
    Convert various date formats into ISO YYYY-MM-DD.
    """
    return parser.parse(date_str).date().isoformat()


def infer_raw_category(description: str) -> str:
    desc = description.lower()

    if "amazon" in desc:
        return "shopping"

    if "uber" in desc:
        return "transport"

    if "salary" in desc:
        return "income"

    if "electricity" in desc:
        return "utilities"

    return "uncategorized"