from langgraph.types import Command
from custom_tools.customer_tools import fetch_orders_history, get_customer_info, get_order_details
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage
from langgraph.types import Command

tools = [get_customer_info, fetch_orders_history, get_order_details]
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)

tools_by_name = {t.name: t for t in tools}

messages = [HumanMessage("Account status for C101, order history for C102, and details for O1003?")]

for _ in range(5):  # hard cap so a confused model can't loop forever
    response = llm.invoke(messages)
    messages.append(response)
    if not response.tool_calls:
        break  # model is done
    for call in response.tool_calls:
        tool = tools_by_name.get(call["name"])
        try:
            if tool is None:
                raise ValueError(f"Unknown tool: {call['name']}")
            result = tool.invoke(call)  # full call, not call["args"]
            if isinstance(result, Command):
                messages.extend(result.update["messages"])
            else:
                messages.append(result)
        except Exception as e:
            messages.append(ToolMessage(f"Error: {e}", tool_call_id=call["id"]))

print(messages[-1].content)