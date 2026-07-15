from mcp.server.fastmcp import FastMCP

from parser import parse_bank_csv

mcp = FastMCP("Bank CSV Parser")


@mcp.tool()
def parse_bank_csv_tool(filepath: str):
    """
    Parse a bank CSV file into validated transactions.
    """
    transactions = parse_bank_csv(filepath)

    return [
        txn.model_dump()
        for txn in transactions
    ]


if __name__ == "__main__":        
    print("Starting MCP server...")
    mcp.run()