from langgraph.checkpoint.sqlite import SqliteSaver

from graph.graph import build_graph

config = {
    "configurable": {
        "thread_id": "phase4_test"
    }
}

with SqliteSaver.from_conn_string(
    "checkpoints/checkpoints.db"
) as checkpointer:

    graph = build_graph(checkpointer)

    state = graph.get_state(config)

    print(state.values)