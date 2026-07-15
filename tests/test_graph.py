from langgraph.checkpoint.sqlite import SqliteSaver

from graph.graph import build_graph
from mcp_server.parser import parse_bank_csv

config = {
    "configurable": {
        "thread_id": "phase4_test"
    }
}

initial_state = {
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

with SqliteSaver.from_conn_string(
    "checkpoints/checkpoints.db"
) as checkpointer:

    graph = build_graph(checkpointer)

    result = graph.invoke(
        initial_state,
        config=config
    )

print("\nCategorized:", len(result["categorized"]))
print("Flagged:", len(result["flagged"]))
print("\nBudget Summary:")
print(result["budget_summary"]["text"])