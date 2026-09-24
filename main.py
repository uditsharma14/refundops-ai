from langchain_core.messages import HumanMessage
from graph.graph import graph
from langchain_core.messages import convert_to_messages


def run(inputs, config):
    """Stream the graph node by node, printing only what each node changed."""
    for update in graph.stream(inputs, config, stream_mode="updates"):
        for node, changes in update.items():
            if node == "__interrupt__":
                continue
            print(f"\n▶ {node}")
            # ToolNode returns a list of updates (one per tool); others return one dict
            for change in changes if isinstance(changes, list) else [changes or {}]:
                for key, value in change.items():
                    if key == "messages":
                        msgs = value if isinstance(value, list) else [value]
                        for msg in convert_to_messages(msgs):
                         msg.pretty_print()
                            
                    else:
                        print(f"   {key}: {value}")


def summary(config):
    snap = graph.get_state(config)
    v = snap.values
    print("\n" + "=" * 45)
    print(f" Order     {v['order_id']}  (customer {v['customer_id']})")
    print(f" Amount    ${v['refund_amount_cents'] / 100:.2f}")
    print(f" Approval  {v.get('approval_status', '-')}")
    print(f" Refund    {v.get('refund_status', '-')}")
    if v.get("error"):
        print(f" Reason    {v['error']}")
    if v.get("reviewer_id"):
        print(f" Reviewer  {v['reviewer_id']}")
    if snap.next:
        print(f" ⏸  Paused before: {snap.next[0]}")
    print("=" * 45)
    return snap


def process(customer_id, order_id, amount_cents, approve=None):
    config = {"configurable": {"thread_id": f"refund-{order_id}"}}
    print(f"\n######## {order_id}: ${amount_cents / 100:.2f} ########")

    run({
        "messages": [HumanMessage(f"Refund order {order_id} for customer {customer_id}")],
        "customer_id": customer_id,
        "order_id": order_id,
        "refund_amount_cents": amount_cents,
    }, config)
    snap = summary(config)

    if snap.next == ("human_review",) and approve is not None:
        decision = "approved" if approve else "rejected"
        print(f"\n👤 Reviewer submits: {decision}")
        graph.update_state(config, {"approval_status": decision, "reviewer_id": "agent_7"})
        run(None, config)  # resume the same thread
        summary(config)


if __name__ == "__main__":
    process("C101", "O1002", 5_000)                 # small → auto-approve
    process("C102", "O1004", 12_000)                # already refunded → reject
    process("C101", "O1008", 15_000, approve=True)  # big → pause, approve, resume