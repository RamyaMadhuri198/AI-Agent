from langgraph.graph import StateGraph, START, END
from agent.nodes import planner_node, tool_caller, analyzer_node, responder_node
from agent.state import AgentState

graph = StateGraph(AgentState)

graph.add_node("planner", planner_node)
graph.add_node("tool_caller",tool_caller)
graph.add_node("analyzer", analyzer_node)
graph.add_node("responder", responder_node)

graph.add_edge(START,"planner")
graph.add_edge("planner","tool_caller")
graph.add_edge("tool_caller", "analyzer")

def route_analyzer(state: AgentState)-> str:
    if state["is_satisfied"]:
        return "responder"
    else:
        return "tool_caller"

graph.add_conditional_edges("analyzer", route_analyzer)
graph.add_edge("responder", END)

app = graph.compile()