import streamlit as st
from agent.graph import app

st.title("MyAgent")
st.caption("Ask me anything — I'll search, calculate and summarize!")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

question = st.text_input("Ask me anything")

if st.button("submit") :
    if len(question) == 0:
        st.warning("Please enter a question before submitting!")
    else:
        with st.spinner("Analyzing"):
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
            try :
                result = app.invoke(initial_state)
                st.session_state["chat_history"].append({"question" : question, "answer" :result["final_answer"]})

            except Exception as e:
                st.error("Something went wrong, please try again.")
    
for history in st.session_state["chat_history"]:
    st.write("You: ", history["question"])
    st.write("Agent: ", history["answer"])