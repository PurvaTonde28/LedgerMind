from copy import deepcopy

from agents.groq_client import client
from agents.prompts import CATEGORIZER_PROMPT
from graph.state import AgentState


def categorizer_node(state: AgentState):

    categorized = []

    for txn in state["transactions"]:

        prompt = CATEGORIZER_PROMPT.format(
            description=txn["description"],
            hint=txn.get("raw_category", "unknown")
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        category = response.choices[0].message.content.strip()

        new_txn = deepcopy(txn)
        new_txn["category"] = category

        categorized.append(new_txn)

    state["categorized"] = categorized

    return state