from mcp_server.parser import parse_bank_csv

from agents.categorizer import categorizer_node
from agents.anomaly_detector import anomaly_node
from agents.budget_advisor import advisor_node

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
state = anomaly_node(state)
state = advisor_node(state)

print("\nBudget Summary:\n")
print(state["budget_summary"]["text"])


# output:
# python -m tests.test_budget     
# WARNING:root:Skipping row 4: Unknown string format: bad_date
# WARNING:root:Skipping row 5: missing amount
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.groq.com/openai/v1/chat/completions "HTTP/1.1 200 OK"

# Budget Summary:

# Shopping is the largest expense. Consider budgeting toreduce it. Cut back on non-essentials.