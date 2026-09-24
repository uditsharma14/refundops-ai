from typing import Annotated, Literal
from typing_extensions import NotRequired, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

from custom_tools.customer_tools import get_customer_info

load_dotenv()

class CustomerRecord(TypedDict):
    customer_id: str
    tier: str
    refunds_last_90d: int
    order_total_cents: int

class RefundGraphState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    customer_id: str
    order_id: str
    refund_amount_cents: int
    customer_history: NotRequired[CustomerRecord]
    approval_status: NotRequired[Literal["pending", "approved", "rejected", "auto_approved"]]
    refund_status: NotRequired[Literal["not_started", "executed", "failed"]]
    reviewer_id: NotRequired[str]
    error: NotRequired[str]