import logging

from graph.state import AgentState

logging.basicConfig(level=logging.INFO)

# Placeholder only — used when no real history is available yet.
# TODO: replace with real checkpointed transaction history once
# Phase 4/5 wires this up to persisted state (see AgentState in Phase 2).
_FALLBACK_CATEGORY_HISTORY = {
    "Shopping": [1200, 1500, 1800, 1400, 1600],
    "Food": [250, 300, 275, 290, 260],
    "Transport": [200, 350, 300, 250, 280],
    "Income": [50000, 52000, 51000, 50500, 49500],
}


def anomaly_node(state: AgentState) -> AgentState:
    flagged = []

    # Real history should live in state (populated from checkpointed
    # past transactions). Falls back to placeholder data if not present,
    # with an explicit warning so this is never silently mistaken for
    # real user history.
    category_history = state.get("category_history")

    if not category_history:
        logging.warning(
            "No real category_history found in state — "
            "using placeholder data. Replace before production use."
        )
        category_history = _FALLBACK_CATEGORY_HISTORY

    for txn in state["categorized"]:

        category = txn["category"]
        amount = abs(txn["amount"])

        history = category_history.get(category, [])

        # Cold start — not enough data to judge "unusual"
        if len(history) < 5:
            continue

        avg = sum(history) / len(history)

        if amount > 2 * avg:
            flagged.append(txn)

    state["flagged"] = flagged

    return state