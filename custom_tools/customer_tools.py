from langchain_core.tools import tool

@tool
def get_customer_info(customer_id: str)-> dict:
    """
    Get customer information based on the provided customer ID.

    Args:
        customer_id (str): The unique identifier for the customer.

    Returns:
        dict: A dictionary containing customer information.
    """
    customers = {
        "C101": {
            "name": "John",
            "refund_count": 1,
            "account_status": "ACTIVE"
        },
        "C102": {
            "name": "Sarah",
            "refund_count": 5,
            "account_status": "ACTIVE"
        }
    }

    return customers.get(
        customer_id,
        {"error": "Customer not found"}
    )