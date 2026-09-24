from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from routing import route_after_validate, route_after_review
from llm.llm import refund_tools

from nodes.nodes import auto_approve, human_review, validate, execute_refund, auto_reject,agent
from state.RefundGraphState import RefundGraphState   # gets the CLASS
# right: import the class itself

print(type(RefundGraphState), list(RefundGraphState.__annotations__))
builder = StateGraph(RefundGraphState)

builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(refund_tools))
builder.add_node("validate", validate)
builder.add_node("auto_approve", auto_approve)
builder.add_node("human_review", human_review)
builder.add_node("execute_refund", execute_refund)
builder.add_node("reject", auto_reject)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: "validate"})
builder.add_edge("tools", "agent")
builder.add_conditional_edges("validate", route_after_validate)
builder.add_edge("auto_approve", "execute_refund")
builder.add_conditional_edges("human_review", route_after_review)
builder.add_edge("execute_refund", END)
builder.add_edge("reject", END)





graph = builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["human_review"],
)
