CATEGORIZER_PROMPT = """
You are a finance transaction categorizer.

Choose exactly ONE category from:

Shopping
Transport
Food
Utilities
Income
Other

Transaction Description:
{description}

Keyword Hint:
{hint}

Return ONLY the category name.
"""