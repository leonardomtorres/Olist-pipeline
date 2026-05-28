import os
os.environ['PGPASSFILE'] = 'nul'
os.environ['PGSYSCONFDIR'] = os.getcwd()

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()

arquivos = {
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_customers_dataset.csv": "customers",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "product_category_translation",
}

def carregar_dados():
    engine = create_engine(
        "postgresql+psycopg2://",
        connect_args={
            "host": os.getenv('POSTGRES_HOST'),
            "port": int(os.getenv('POSTGRES_PORT')),
            "dbname": os.getenv('POSTGRES_DB'),
            "user": os.getenv('POSTGRES_USER'),
            "password": os.getenv('POSTGRES_PASSWORD'),
        }
    )

    for arquivo, tabela in arquivos.items():
        caminho = f"data/raw/{arquivo}"
        print(f"carregando {tabela}...")

        df = pd.read_csv(caminho)
        df.to_sql(tabela, con=engine, schema="raw", if_exists="replace", index=False)

        print(f"{tabela} ok - {len(df)} linhas")

if __name__ == "__main__":
    carregar_dados()