from typing import TypedDict, List

class AgentState(TypedDict):
    user_question : str
    needs_tool : bool
    tool_to_use : str
    tool_output : str
    is_satisfied : bool
    final_answer : str
    messages: List[str]
    iteration_count: int    
