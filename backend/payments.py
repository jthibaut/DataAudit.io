# backend/payments.py
import os
import stripe
from urllib.parse import quote_plus

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

def create_checkout_session(email: str, file_url: str, price_eur: float = 4.99) -> str:
    """
    Crée une session Stripe Checkout et renvoie l'URL de redirection.
    - price_eur : montant en euros (float)
    - file_url : URL publique du rapport (sera placée en metadata)
    """
    if not stripe.api_key:
        raise RuntimeError("Stripe API key not configured")

    # price in cents
    amount_cents = int(round(price_eur * 100))

    # success & cancel URLs — à adapter selon ton frontend déployé
    success_url = os.getenv("SUCCESS_URL", "https://your-streamlit-frontend/success")
    cancel_url = os.getenv("CANCEL_URL", "https://your-streamlit-frontend/cancel")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": "DataAudit - Rapport"},
                "unit_amount": amount_cents,
            },
            "quantity": 1,
        }],
        metadata={
            "email": email,
            "file_url": file_url,
        },
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url
