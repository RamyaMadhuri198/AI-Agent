from agent.graph import app

question = "my car is going back when i put the gear in drive mode it a new car car 4 months old, it happened twice and i apply the gear facctly why ?" \
""

initial_state = {
    "user_question" : question,
    "needs_tool" : None,
    "tool_to_use" : None,
    "tool_output" : None,
    "is_satisfied" : None,
    "final_answer" : None,
    "messages": [],
    "iteration_count" :0

}

result = app.invoke(initial_state)
print(result["final_answer"])

