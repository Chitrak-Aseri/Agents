def generate(context: AgentContext) -> AgentContext:
    if not context.should_generate:
        return context

    # Generate issues (title, body)
    issues = [
        {"title": "Fix missing docstrings", "body": "...details..."},
        {"title": "Update JSON schema", "body": "..."}
    ]
    context.generated_issues = issues
    return context
