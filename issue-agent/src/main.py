from graph.graph_builder import build_graph
from core.loader import load_docs, load_issues
from core.context import AgentContext
from utils.github import create_issues

if __name__ == "__main__":
    context = AgentContext()
    context.docs = load_docs()
    context.issues = load_issues()

    graph = build_graph()
    final_state = graph.invoke(context)

    if final_state.generated_issues:
        create_issues(final_state.generated_issues)
