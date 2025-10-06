import os
import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_checkout_session(success_url: str, cancel_url: str, price_cents: int = 900):
    if not stripe.api_key:
        raise RuntimeError("Stripe API key not set. Configure STRIPE_API_KEY in .env")

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': 'DataAudit - Rapport unique'},
                'unit_amount': price_cents,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session.url