from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from graph.graph import build_graph

config = {
    "configurable": {
        "thread_id": "phase5_test_noflag"
    }
}

with SqliteSaver.from_conn_string(
    "checkpoints/checkpoints.db"
) as checkpointer:

    graph = build_graph(checkpointer)

    result = graph.invoke(
        Command(
            resume={
                "approved": False
            }
        ),
        config=config,
    )

print("\nResumed Result:\n")
print(result)

print("\nUser Decisions:")
print(result["user_decisions"])

print("\nBudget Summary:")
print(result["budget_summary"]["text"])