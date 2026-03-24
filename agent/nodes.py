from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from agent.state import AgentState
from dotenv import load_dotenv
import os
from ddgs import DDGS
import io
import contextlib

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

#planner node
def planner_node(state : AgentState) ->AgentState:
    question = state["user_question"]
    system_prompt = """
You are a planner agent. Your job is to analyze 
the user's question and decide:

1. Does this question require a tool to answer?
   - Use web_search if the question needs current 
     or realtime information
   - Use python_repl if the question needs 
     calculations or data analysis
   - Use summarizer if the question needs 
     long text to be summarized
   - Use none if you can answer directly 
     without any tool

2. Respond in this EXACT format and nothing else:
   needs_tool: true or false
   tool_to_use: web_search / python_repl / summarizer / none
"""

    response = llm.invoke([
        SystemMessage(content = system_prompt),
        HumanMessage(content = question)
    ])

    response_text = response.content

    #LLM response on tool use
    needs_tool = "true" in response_text.lower()

    # LLM response on which tool

    tool_to_use ="none"

    if "web_search" in response_text.lower():
        tool_to_use = "web_search"
    elif "python_repl" in response_text.lower():
        tool_to_use = "python_repl"
    elif "summarizer" in response_text.lower() :
        tool_to_use = "summarizer"

    return {
        "needs_tool" :needs_tool,
        "tool_to_use" : tool_to_use,
        "messages" : state["messages"] + [response_text]

    }

# Tool Caller Node

def tool_caller(state : AgentState) ->AgentState:
    tool = state["tool_to_use"]

    question = state["user_question"]


    if tool.lower() == "web_search":
        with DDGS() as ddgs:
            results = ddgs.text(question, max_results=5)

        result ="\n".join([r["body"] for r in results])

    elif tool.lower() == "python_repl":
        system_prompt = """
1. You are a python programmer.
2. your job is to analyze the user's question and write a python code to answer the user question
3. Return ONLY the raw Python code with NO explanations, NO markdown, NO backticks.
4. The code must be directly executable.
"""
        response = llm.invoke([
            SystemMessage(content = system_prompt),
            HumanMessage(content = question),
        ])

        response_text = response.content

        output = io.StringIO()
        namespace = {}
        with contextlib.redirect_stdout(output):
            exec(response_text, namespace)

        result = output.getvalue()

    elif tool.lower() == "summarizer":
        system_prompt = """
1. you are a summarizer
2. your job is to analyze the user's question and provide a concise summary of the topic
3. Return only summarized output and nothing else
"""
        response = llm.invoke ([
            SystemMessage(content = system_prompt),
            HumanMessage(content = question)
        ])

        response_text = response.content

        result = response_text

    else :
        system_prompt ="""
1. you are a helpful assistant
2. your job is to analyze the user's question and answer the user's question directly
3. Return the answer only and nothing else
"""
        response = llm.invoke([
            SystemMessage(content = system_prompt),
            HumanMessage(content = question),
        ])
        response_text = response.content
        result = response_text

    return {
        "tool_output": result,
        "messages" : state["messages"] + [result]
    }

# Analyzer node

def analyzer_node(state : AgentState) -> AgentState:
    tool_output = state["tool_output"]
    question = state["user_question"]
    system_prompt = """
1. Your role is analyzer.
2. your job is to read the User's question and analyze the answer and decide wheather you have satified or not with the answer.
3. Respond in this EXACT format and nothing else:
   is satisfied = yes / No
"""
    response = llm.invoke([
    SystemMessage(content=system_prompt),
    HumanMessage(content=f"User Question : {question}\nResult : {tool_output}")
    
])

    response_text = response.content

    satisfied = True if "yes" in response_text.lower() else False

    current_count = state["iteration_count"] + 1

    # Force stop after 5 iterations
    if current_count >= 5:
        satisfied = True
    
    return {
        "is_satisfied" : satisfied,
        "iteration_count": current_count,
        "messages" : state["messages"] + [response_text]
        
    }

# Responder node
def responder_node(state : AgentState) -> AgentState:
    question = state["user_question"]
    tool_output = state["tool_output"]

    system_prompt = """
1. you are a responder.
2. your job is to analyze the User's question and the given results, then write a clean final answer 
3. Return final answer only with no other symbols at start and end and nothing else
"""
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content = f"User's Question : {question}\nResult : {tool_output}")
    ])

    response_text = response.content

    return {
        "final_answer" : response_text,
        "messages" : state["messages"] + [response_text]
    }

    
 