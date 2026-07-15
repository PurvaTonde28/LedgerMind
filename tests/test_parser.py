from parser import parse_bank_csv

transactions = parse_bank_csv(
    "sample_data/bank_sample.csv"
)

for t in transactions:
    print(t.model_dump())


# output after executing this file :
# WARNING:root:Skipping row 4: Unknown string format: bad_date
# {'date': '2025-06-01', 'description': 'Amazon Purchase', 'amount': -1450.25, 'raw_category': 'shopping'}
# {'date': '2025-06-02', 'description': 'Salary', 'amount': 55000.0, 'raw_category': 'income'}
# {'date': '2025-06-03', 'description': 'Uber Trip', 'amount': -320.0, 'raw_category': 'transport'}
# {'date': '2025-06-05', 'description': 'Starbucks', 'amount': -280.0, 'raw_category': 'uncategorized'}
# {'date': '2025-06-08', 'description': 'Electricity Bill', 'amount': nan, 'raw_category': 'utilities'}