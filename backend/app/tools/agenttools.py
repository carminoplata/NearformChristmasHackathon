from google.adk.tools.tool_context import ToolContext

def ask_confirmation(query: str, tool_context: ToolContext) -> str:
    if not query or len(query) == 0:
        raise ValueError("No query available.")
    if not tool_context.tool_confirmation:
        tool_context.request_confirmation(
            hint=f"""Can I search offers for these products?: 
                {query}""",
            payload=query
        )
        return { "status": "pending",
                 "message": "Waiting for user confirmation"
        }
    if tool_context.tool_confirmation.confirmed:
        return {
            "status": "approved",
            "query": query,
            "message": "User confirmed the query."
        }
    else:
        return {
            "status": "rejected",
            "message": "User rejected the query."
        }
