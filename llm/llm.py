import os

from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from custom_tools.customer_tools import (
    fetch_orders_history,
    get_customer_info,
    get_order_details,
)

load_dotenv()

refund_tools = [ fetch_orders_history, get_customer_info, get_order_details]

MODEL_NAME = os.getenv("REFUND_MODEL", "gpt-4o-mini")

def build_chat_model():
    """Build and return a ChatOpenAI model using the specified model name."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
 
    model = ChatOpenAI(
        model=MODEL_NAME,
        temperature=0,   # predictable tool-calling for a money workflow
        timeout=30,      # don't let one slow API call hang a thread forever
        max_retries=2,   # retry transient network/rate-limit errors
        api_key=api_key,
    )
    return model.bind_tools(refund_tools)