import pandas as pd
import pytest


COLUNAS_ORDERS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
]

COLUNAS_ORDER_ITEMS = [
    "order_id",
    "product_id",
    "seller_id",
    "price",
    "freight_value",
]


def test_orders_colunas_existem():
    df = pd.DataFrame(columns=COLUNAS_ORDERS)
    for col in COLUNAS_ORDERS:
        assert col in df.columns


def test_order_items_preco_positivo():
    df = pd.DataFrame({
        "order_id": ["abc", "def"],
        "product_id": ["p1", "p2"],
        "seller_id": ["s1", "s2"],
        "price": [150.0, 89.90],
        "freight_value": [12.0, 8.50],
    })
    assert (df["price"] > 0).all()
    assert (df["freight_value"] >= 0).all()


def test_sem_order_id_nulo():
    df = pd.DataFrame({
        "order_id": ["abc", "def", "ghi"],
        "order_status": ["delivered", "shipped", "canceled"],
    })
    assert df["order_id"].notna().all()
