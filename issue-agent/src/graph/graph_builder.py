from langgraph.graph import StateGraph, END
from agents.review_agent import review
from agents.generator_agent import generate

def build_graph():
    builder = StateGraph(AgentContext)
    builder.add_node("review", review)
    builder.add_conditional_edges(
        "review",
        lambda context: "generate" if context.should_generate else END,
        {"generate": "generate", END: END},
    )
    builder.add_node("generate", generate)
    builder.set_entry_point("review")
    return builder.compile()
