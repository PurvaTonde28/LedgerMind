from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    transactions: List[dict]
    categorized: List[dict]
    flagged: List[dict]
    user_decisions: List[dict]
    budget_summary: Optional[dict]
    category_history: Optional[dict]