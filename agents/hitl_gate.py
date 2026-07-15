from langgraph.types import interrupt

from graph.state import AgentState


def hitl_gate_node(state: AgentState) -> AgentState:
    decisions = list(state.get("user_decisions", []))

    for txn in state["flagged"]:

        decision = interrupt(
            {
                "action": "approve_or_reject_flag",
                "transaction": txn,
            }
        )

        decisions.append(
            {
                "transaction": txn,
                "approved": decision.get("approved"),
            }
        )

    state["user_decisions"] = decisions

    return state