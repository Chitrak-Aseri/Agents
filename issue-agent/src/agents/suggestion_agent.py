from langchain_core.prompts import ChatPromptTemplate

def generate_contextual_suggestion(llm, code: str, issue_body: str):
    prompt = ChatPromptTemplate.from_template("""
        You are an AI code reviewer.

        HERE IS THE CODEBASE


        {code}

        You have been provided with the body of a GitHub issue that has been created:
        An issue has been created stating:
        "{issue_body}"

        Write a code-aware comment about how this issue might be addressed. Refer to exact patterns, suggest refactors, best practices, or missing logic if any.
    """)
    chain = prompt | llm
    return chain.invoke({
        "code": code,  # Optional truncation
        "issue_body": issue_body
    })
