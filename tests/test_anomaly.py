from mcp_server.parser import parse_bank_csv

from agents.categorizer import categorizer_node
from agents.anomaly_detector import anomaly_node

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
    "category_history": None,  # no real history yet -> triggers fallback warning
}

state = categorizer_node(state)
state = anomaly_node(state)

print("Flagged Transactions:\n")

for txn in state["flagged"]:
    print(txn)

# Expected: a WARNING log line about placeholder history appears first,
# making explicit that this run used fallback data, not real history.

# output 1 with    '2025-06-01,Amazon Purchase,-1450.25'
# python -m tests.test_anomaly    
# WARNING:root:Skipping row 4: Unknown string format: bad_date
# WARNING:root:Skipping row 5: missing amount
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# Flagged Transactions: 


# output 2 with  '2025-06-01,Amazon Purchase,-4500'
# python -m tests.test_anomaly
# WARNING:root:Skipping row 4: Unknown string format: bad_date
# WARNING:root:Skipping row 5: missing amount
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# Flagged Transactions:

# {'date': '2025-06-01', 'description': 'Amazon Purchase', 'amount': -4500.0, 'raw_category': 'shopping', 'category': 'Shopping'}