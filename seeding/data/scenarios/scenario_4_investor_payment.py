from app.models.enums.payment import PaymentMethod, PaymentDirection

SCENARIO_4_INVESTOR_PAYMENT = {
    "name": "Scenario 4: Initial Investor Payment",
    "recorder_username": "admin",
    "investor_username": "sara", # The new investor
    "payments": [
        {
            "payment_method": PaymentMethod.CARD_TRANSACTION,
            "direction": PaymentDirection.INCOMING,
            "description": "سرمایه گذاری اولیه توسط خانم محمدی",
            "amount": 5_000_000_000, # 500 Million Toman
        }
    ]
}
