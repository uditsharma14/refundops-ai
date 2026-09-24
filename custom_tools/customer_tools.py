import json
from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.types import Command

from model.mock.customer import CUSTOMERS
from model.mock.orders import ORDERS, ORDERS_HISTORY


def _result(field: str, record: dict, tool_call_id: str) -> Command:
    """Every tool must update its own state field AND answer the tool call."""
    return Command(update={
        field: record,
        "messages": [ToolMessage(json.dumps(record), tool_call_id=tool_call_id)],
    })


@tool
def get_customer_info(
    customer_id: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Look up a customer's account status. Call this for every refund request."""
    record = CUSTOMERS.get(customer_id) or {"error": f"Customer {customer_id} not found"}
    return _result("customer_history", record, tool_call_id)


@tool
def fetch_orders_history(
    customer_id: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Get a customer's past orders and refund count. Call this for every refund
    request to check how often the customer has requested refunds."""
    record = ORDERS_HISTORY.get(customer_id) or {"error": f"Customer {customer_id} not found"}
    return _result("order_history", record, tool_call_id)


@tool
def get_order_details(
    order_id: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Get the order being refunded: owner, status and amount. Call this for
    every refund request."""
    record = ORDERS.get(order_id) or {"error": f"Order {order_id} not found"}
    return _result("order_details", record, tool_call_id)