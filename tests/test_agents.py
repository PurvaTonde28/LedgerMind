"""
Full Phase 3 chain test: transactions -> categorized -> flagged -> budget_summary
Run with: python -m tests.test_agents
"""
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
    "category_history": None,
}

state = categorizer_node(state)
assert len(state["categorized"]) > 0, "Categorizer produced no output"

state = anomaly_node(state)
# flagged may legitimately be empty — not an assertion failure

state = advisor_node(state)
assert state["budget_summary"] is not None, "Budget advisor produced no output"

print("=== Categorized ===")
for txn in state["categorized"]:
    print(txn)

print("\n=== Flagged ===")
for txn in state["flagged"]:
    print(txn)

print("\n=== Budget Summary ===")
print(state["budget_summary"]["text"])