from custom_tools.customer_tools import get_customer_info
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, ToolMessage

tools = [get_customer_info]
llm = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)
tools_by_name = {t.name: t for t in tools}

messages = [HumanMessage("What's the account status for customer C101?")]

# 1. Ask the model — it decides whether to call a tool
response = llm.invoke(messages)
messages.append(response)

# 2. If it requested tool calls, run them and feed results back
for call in response.tool_calls:
    result = tools_by_name[call["name"]].invoke(call["args"])
    messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

# 3. Call the model again so it can use the tool output to answer
final = llm.invoke(messages)
print(final.content)
