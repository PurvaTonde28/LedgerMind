from langgraph.checkpoint.sqlite import SqliteSaver

from graph.graph import build_graph

config = {
    "configurable": {
        
        "thread_id": "user223"
    }
}

with SqliteSaver.from_conn_string("checkpoints/checkpoints.db") as checkpointer:
    graph = build_graph(checkpointer)

    graph.invoke(
        {
            "transactions": [{"desc": "Books"}],
            "categorized": [],
            "flagged": [],
            "user_decisions": [],
            "budget_summary": None,
        },
        config=config,
    )

    state = graph.get_state(config)

    print(state.values)


# output: 
# Dummy node executed
# [{'desc': 'Coffee'}]
# {'transactions': [{'desc': 'Coffee'}], 'categorized': [], 'flagged': [], 'user_decisions': [], 'budget_summary': None}