## Phase 2 — State & Persistence
Shared `AgentState` (TypedDict) passed through the graph. Uses LangGraph's 
`SqliteSaver` checkpointer, keyed by `thread_id`, for cross-session memory — 
verified by killing the Python process and confirming state resumes correctly 
on a fresh run via `get_state()`.