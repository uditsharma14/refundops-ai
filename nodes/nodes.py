from urllib import response

from langchain_core.messages import SystemMessage, AIMessage
from state import RefundGraphState
from llm.llm import build_chat_model

llm = build_chat_model()


SYSTEM = SystemMessage(content=(
    "You gather information for refund requests. "
    "Call get_customer_info, fetch_orders_history and get_order_details. "
    "Do not approve or reject anything."
))

def agent(refundState : RefundGraphState) -> dict:
    """Decides which lookups to run. Never makes the refund decision."""
    response = llm.invoke([SYSTEM] + refundState["messages"])
    return {"messages": [response]}


def validate(refundState: RefundGraphState) -> dict:
    """Validates the refund request based on customer and order details."""
    customer = refundState.get("customer_history") or {}
    order = refundState.get("order_details") or {}
    amount = refundState["refund_amount_cents"]
    problems = []

    if not customer or "error" in customer:
        problems.append("customer not found")
    elif customer.get("account_status") != "ACTIVE":
        problems.append("account is not active")

    if not order or "error" in order:
        problems.append("order not found")

    else :
        if customer.get("customer_id")!= order.get("customer_id"):
           problems.append("customer and order do not match")
        if  order.get("status") != "COMPLETED":
           problems.append("order is not completed")
        if order.get("already_refunded"):
           problems.append("order has already been refunded")
        if amount <= 0:
            problems.append("refund amount must be positive")
        elif amount > order.get("total_amount_cents"):
            problems.append("refund amount excee" \
            "ds order total")
    

    if problems:
       return {"approval_status": "rejected", "problems": "".join(problems)}
    
    return {"approval_status": "pending"}

def execute_refund(refundState: RefundGraphState) -> dict:
    """Executes the refund process based on the approval status."""
    if refundState.get("refund_status") == "executed":
        return {}  # idempotency: a resumed or retried thread must not pay twice 
    if refundState.get("approval_status") not in ("approved", "auto_approved"):
        return {"refund_status": "failed", "error": "refund not approved"}
     # payment_api.refund(state["order_id"], state["refund_amount_cents"],
    #                    idempotency_key=state["order_id"])
    return {"refund_status": "executed",
            "messages": AIMessage(content=f"refund for {refundState.get('order_details', {}).get('order_id')} was executed")}


def auto_approve(refundState: RefundGraphState) -> dict:
        """Automatically approves the refund without any validation."""
        return {"approval_status": "approved"}


def human_review(refundState: RefundGraphState) -> dict:
        """Requires human review for the refund."""
        if not refundState.get("approval_status") not in ["approved", "rejected"]:
            return {"approval_status": "rejected",
                "error": "resumed without a reviewer decision"}
        if refundState.get("approval_status") == "approved" and not refundState.get("reviewer_id") :
            return {"approval_status": "rejected",
                "error": "approved without a reviewer decision"}
        if refundState.get("approval_status") == "rejected":
            return {"approval_status": "rejected"}
        return {}
    
def auto_reject(refundState: RefundGraphState) -> dict:
        """Automatically rejects the refund without any validation."""
        reason = refundState.get("error") or "declined by reviewer"
        return {"approval_status": "rejected",
                "messages": AIMessage(content=f"refund for {refundState.get('order_details', {}).get('order_id')} was rejected: {reason}")}