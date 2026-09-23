from custom_tools.customer_tools import fetch_user_history, get_customer_info, get_order_details
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

tools = [get_customer_info, fetch_user_history, get_order_details]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
tools_by_name = {t.name: t for t in tools}

messages = [HumanMessage("What's the account status for customer C101?")]
messages.append(HumanMessage("Also, what's the order history for customer C102?"))
messages.append(HumanMessage("Also, what are the details for order O1003?"))
# 1. Ask the model — it decides whether to call a tool
response = llm.invoke(messages)
messages.append(response)

# 2. If it requested tool calls, run them and feed results back
for call in response.tool_calls:
    #print(f"Tool call: {call['name']} with args {call['args']}")
    result = tools_by_name[call["name"]].invoke(call["args"])
    messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

# 3. Call the model again so it can use the tool output to answer
final = llm.invoke(messages)
print(final.content)
