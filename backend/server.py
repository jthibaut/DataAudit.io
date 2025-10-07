# backend/server.py
import os
import logging
import stripe
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .payments import create_checkout_session as create_session
from .emailer import send_report_email

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="DataAudit.io Backend")

# CORS - en prod, remplace "*" par l'URL de ton frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Stripe init
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")

# Models
class CheckoutRequest(BaseModel):
    email: str
    file_url: str
    price_eur: float = 4.99  # montant en euros, modifiable

@app.post("/create-checkout-session")
async def create_checkout_session(payload: CheckoutRequest):
    """
    Crée une session Stripe Checkout.
    Attendre le paiement via webhook pour envoyer le rapport par email.
    """
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="Stripe API key not configured")

    try:
        session_url = create_session(
            email=payload.email,
            file_url=payload.file_url,
            price_eur=payload.price_eur,
        )
        return {"url": session_url}
    except Exception as e:
        logger.exception("Erreur création session Stripe")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Endpoint pour recevoir les webhooks Stripe.
    Configure STRIPE_WEBHOOK_SECRET dans l'environnement.
    """
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    if not webhook_secret:
        logger.error("STRIPE_WEBHOOK_SECRET not set")
        raise HTTPException(status_code=500, detail="Webhook secret not configured")

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=webhook_secret)
    except Exception as e:
        logger.exception("Invalid webhook signature")
        raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {e}")

    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session.get("metadata", {})
        email = metadata.get("email")
        file_url = metadata.get("file_url")

        if email and file_url:
            # send report email asynchronously (simple approach)
            try:
                send_report_email(recipient=email, report_url=file_url)
                logger.info(f"Sent report to {email} for file {file_url}")
            except Exception as e:
                logger.exception("Failed to send email after checkout")
        else:
            logger.warning("Missing email or file_url in session metadata")

    return {"status": "success"}


@app.get("/health")
async def health():
    return {"status": "ok"}
