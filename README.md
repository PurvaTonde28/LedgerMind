## Phase 1 - MCP Server — Bank CSV Parser
Exposes a `parse_bank_csv_tool` via MCP (stdio transport) that parses bank 
transaction CSVs into validated Pydantic models. Malformed rows (bad dates, 
missing amounts) are skipped and logged rather than crashing the pipeline.
Tested independently via MCP Inspector before agent integration.

## Phase 2 — State & Persistence
Shared `AgentState` (TypedDict) passed through the graph. Uses LangGraph's 
`SqliteSaver` checkpointer, keyed by `thread_id`, for cross-session memory — 
verified by killing the Python process and confirming state resumes correctly 
on a fresh run via `get_state()`.

## Phase 3 — Sub-Agents
Categorizer, anomaly-detector, and budget-advisor agents implemented and 
chained. Categorizer uses Groq (temp=0) to override/confirm Phase 1's 
keyword-based category hints — verified on a real case (Starbucks: 
hint "uncategorized" → correctly assigned "Food"). Anomaly detection is 
a static, LLM-free rule (flag if >2x category rolling average, skip if 
<5 historical points) — currently using placeholder category history 
with an explicit runtime warning; real checkpointed history integration 
is planned for a later phase.

## Phase 4 — Supervisor & Conditional Routing
Replaced manual node-chaining test scripts with a real LangGraph supervisor 
(`categorizer` → `anomaly` → conditional edge → `advisor` → `END`), compiled 
with the Phase 2 SQLite checkpointer.

The conditional edge (`route_after_anomaly`) inspects `state["flagged"]` at 
runtime — both branches currently route to `advisor` (real branching to a 
`hitl_gate` node is Phase 5), but the routing mechanism itself is real and 
verified: two separate runs (`flagged: 0` vs `flagged: 1`, forced by 
changing the input amount) confirmed the graph reads live state to decide 
routing, not a hardcoded path.

Restart persistence was re-verified on this full multi-node graph (not just 
the Phase 2 dummy node) — `test_resume.py`, run as a separate process after 
`test_graph.py`, correctly retrieved the exact final state (including the 
flagged transaction) from disk via `get_state()`, confirming checkpointing 
survives the added routing complexity.

## Phase 5 — Human-in-the-Loop Gate
Added a `hitl_gate` node using LangGraph's `interrupt()`. When a transaction 
is flagged, the graph genuinely pauses execution and persists at that point 
via the checkpointer — verified by invoking, resuming, and rejecting across 
three separate process invocations (not a single continuous script), each 
confirmed via `Command(resume=...)` on a fresh process. Approve, reject, 
and no-flag (skip-gate) paths all verified independently.