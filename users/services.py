import os

import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_product_stripe():
    """Создание продукта."""

    return stripe.Product.create(name="New_Product")


def create_stripe_price_amount(product_name: str, amount: int) -> dict:
    """Создание цены."""

    return stripe.Price.create(currency="usd", unit_amount=amount * 100, product_data={"name": product_name})


def create_stripe_session(price: dict) -> tuple:
    """Создание сессии."""

    session = stripe.checkout.Session.create(
        success_url=os.getenv("SUCCESS_URL_SESSION"),
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
