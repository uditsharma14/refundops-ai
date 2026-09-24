from state import RefundGraphState


def route_after_validate(state: RefundGraphState) -> str:
    if state.get("error"):
        return "reject"
    if state["refund_amount_cents"] < 10_000:
        return "auto_approve"
    return "human_review"


def route_after_review(state: RefundGraphState) -> str:
    return "execute_refund" if state.get("approval_status") == "approved" else "reject"