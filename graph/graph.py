from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.categorizer import categorizer_node
from agents.anomaly_detector import anomaly_node
from agents.budget_advisor import advisor_node
from agents.hitl_gate import hitl_gate_node

def route_after_anomaly(state: AgentState) -> str:

    if state.get("flagged"):
        return "hitl_gate"

    return "advisor"


def build_graph(checkpointer):

    builder = StateGraph(AgentState)

    builder.add_node("categorizer", categorizer_node)
    builder.add_node("anomaly", anomaly_node)
    builder.add_node("hitl_gate", hitl_gate_node)
    builder.add_node("advisor", advisor_node)

    builder.set_entry_point("categorizer")

    builder.add_edge("categorizer", "anomaly")
    builder.add_edge("hitl_gate", "advisor")
    builder.add_edge("advisor", END)
    
    builder.add_conditional_edges(
        "anomaly",
        route_after_anomaly,
        {
            "hitl_gate": "hitl_gate",
            "advisor": "advisor",
        },
    )

    

    return builder.compile(checkpointer=checkpointer)