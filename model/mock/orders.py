ORDERS_HISTORY = {
        "C101": {
            "refund_count": 1,
            "orders": [
                {"order_id": "O1001", "status": "REFUNDED"},
                {"order_id": "O1002", "status": "DELIVERED"}
            ]
        },
        "C102": {
            "refund_count": 5,
            "orders": [
                {"order_id": "O1003", "status": "REFUNDED"},
                {"order_id": "O1004", "status": "REFUNDED"},
                {"order_id": "O1005", "status": "REFUNDED"},
                {"order_id": "O1006", "status": "REFUNDED"},
                {"order_id": "O1007", "status": "DELIVERED"}
            ]
        }
    }


ORDERS = {
        "O1001": {
            "customer_id": "C101",
            "status": "REFUNDED",
            "amount": 100.0
        },
        "O1002": {
            "customer_id": "C101",
            "status": "DELIVERED",
            "amount": 50.0
        },
        "O1003": {
            "customer_id": "C102",
            "status": "REFUNDED",
            "amount": 75.0
        },
        "O1004": {
            "customer_id": "C102",
            "status": "REFUNDED",
            "amount": 120.0
        },
        "O1005": {
            "customer_id": "C102",
            "status": "REFUNDED",
            "amount": 200.0
        },
        "O1006": {
            "customer_id": "C102",
            "status": "REFUNDED",
            "amount": 150.0
        },
        "O1007": {
            "customer_id": "C102",
            "status": "DELIVERED",
            "amount": 80.0
        }
    }