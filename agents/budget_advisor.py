from agents.groq_client import client
from graph.state import AgentState


def advisor_node(state: AgentState) -> AgentState:

    totals = {}

    for txn in state["categorized"]:
        category = txn["category"]

        # Ignore income in spending summary
        if category == "Income":
            continue

        totals[category] = totals.get(category, 0) + abs(txn["amount"])

    prompt = f"""
You are a personal finance assistant.

Category totals:

{totals}

Write a short (2-3 sentence) budget summary.

Mention:
1. Largest spending category.
2. One practical suggestion to reduce expenses.

Your suggestion must relate directly to the largest category identified above.

Keep it under 60 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    state["budget_summary"] = {
        "text": response.choices[0].message.content.strip()
    }

    return state