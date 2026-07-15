from mcp_server.parser import parse_bank_csv

from agents.categorizer import categorizer_node

state = {
    "transactions": [
        txn.model_dump()
        for txn in parse_bank_csv(
            "mcp_server/sample_data/bank_sample.csv"
        )
    ],
    "categorized": [],
    "flagged": [],
    "user_decisions": [],
    "budget_summary": None,
}

state = categorizer_node(state)

for txn in state["categorized"]:
    print(txn)


# output : 
# WARNING:root:Skipping row 4: Unknown string format: bad_date
# WARNING:root:Skipping row 5: missing amount
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# {'date': '2025-06-01', 'description': 'Amazon Purchase', 'amount': -1450.25, 'raw_category': 'shopping', 'category': 'Shopping'}
# {'date': '2025-06-02', 'description': 'Salary', 'amount': 55000.0, 'raw_category': 'income', 'category': 'Income'}
# {'date': '2025-06-03', 'description': 'Uber Trip', 'amount': -320.0, 'raw_category': 'transport', 'category':'Transport'}
# {'date': '2025-06-05', 'description': 'Starbucks', 'amount': -280.0, 'raw_category': 'uncategorized', 'category': 'Food'}