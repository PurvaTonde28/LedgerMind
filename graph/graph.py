from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.categorizer import categorizer_node
from agents.anomaly_detector import anomaly_node
from agents.budget_advisor import advisor_node


def route_after_anomaly(state: AgentState) -> str:
    """
    Phase 4:
    Routing exists, but both paths go to advisor.

    Phase 5:
    if flagged -> hitl_gate
    else -> advisor
    """

    if state.get("flagged"):
        return "advisor"

    return "advisor"


def build_graph(checkpointer):

    builder = StateGraph(AgentState)

    builder.add_node("categorizer", categorizer_node)
    builder.add_node("anomaly", anomaly_node)
    builder.add_node("advisor", advisor_node)

    builder.set_entry_point("categorizer")

    builder.add_edge("categorizer", "anomaly")

    builder.add_conditional_edges(
        "anomaly",
        route_after_anomaly,
        {
            "advisor": "advisor"
        }
    )

    builder.add_edge("advisor", END)

    return builder.compile(checkpointer=checkpointer)