# MCP Server — Bank CSV Parser
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