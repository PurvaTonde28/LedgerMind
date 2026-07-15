# MCP Server — Bank CSV Parser
Exposes a `parse_bank_csv_tool` via MCP (stdio transport) that parses bank 
transaction CSVs into validated Pydantic models. Malformed rows (bad dates, 
missing amounts) are skipped and logged rather than crashing the pipeline.
Tested independently via MCP Inspector before agent integration.