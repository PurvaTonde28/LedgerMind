from langgraph.graph import StateGraph, END

from graph.state import AgentState


def dummy_node(state: AgentState):
    print("Dummy node executed")
    print(state.get("transactions"))
    return state


def build_graph(checkpointer):
    builder = StateGraph(AgentState)

    builder.add_node("dummy", dummy_node)
    builder.set_entry_point("dummy")
    builder.add_edge("dummy", END)

    return builder.compile(checkpointer=checkpointer)