import json
from typing import Annotated
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.tools import InjectedToolCallId, tool
from model.mock.customer import CUSTOMERS
from model.mock.orders import ORDERS, ORDERS_HISTORY


@tool
def get_customer_info(
    customer_id: str,
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Look up a customer's account. Call this first for every refund request."""
    record = CUSTOMERS.get(customer_id)
    if record is None:
        record = {"error": f"Customer {customer_id} not found"}
    return Command(update={
        "customer_history": record,
        "messages": [ToolMessage(json.dumps(record), tool_call_id=tool_call_id)],
    })


@tool
def fetch_orders_history(user_id: str, 
        tool_call_id: Annotated[str, InjectedToolCallId])-> Command:
    """
    Get the order history for a specific user based on their ID.
    Args:
        user_id (str): The unique identifier for the user."""

    record = ORDERS_HISTORY.get(user_id)
    if record is None:
        record = {"error": f"User {user_id} not found"}
    return Command(update={
        "customer_history": record,
        "messages": [ToolMessage(json.dumps(record), tool_call_id=tool_call_id)],
    })


@tool
def get_order_details(order_id: str, 
    tool_call_id: Annotated[str, InjectedToolCallId]) -> Command:
    """
    Get the details of a specific order based on its ID.

    Args:
        order_id (str): The unique identifier for the order.

    Returns:
        dict: A dictionary containing order details.
    """
    record = ORDERS.get(order_id)
    if record is None:
         record ={"error": f"Order {order_id} not found"}
    return Command(update={
        "customer_history": record,
        "messages": [ToolMessage(json.dumps(record), tool_call_id=tool_call_id)],
    })