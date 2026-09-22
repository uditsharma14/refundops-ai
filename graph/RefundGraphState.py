import os
from typing import Annotated, Optional, TypedDict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages

from custom_tools.customer_tools import get_customer_info

load_dotenv()


class RefundGraphState(TypedDict):
    messages: Annotated[list, add_messages]
    customer_id: str
    order_id: str
    refund_amount: float
    customer_history: Optional[dict]
    refund_status: Optional[str]
    approval_status: Optional[str]


refund_tools = [get_customer_info]


def build_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return ChatOpenAI(model="gpt-4o-mini", api_key=api_key).bind_tools(refund_tools)


llm = build_llm()

__all__ = ["RefundGraphState", "refund_tools", "build_llm", "llm"]
