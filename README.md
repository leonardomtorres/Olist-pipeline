# Olist Data Pipeline

Pipeline de engenharia de dados end-to-end usando o dataset público da Olist. Cobre desde a ingestão dos CSVs até um dashboard com os dados transformados.

## Stack

- Python + pandas + SQLAlchemy (ingestão)
- PostgreSQL 15 (armazenamento)
- dbt-core (transformações)
- Docker + Docker Compose (infraestrutura)
- Streamlit + Plotly (dashboard)
- GitHub Actions (CI)
- pytest (testes)

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 9 tabelas, ~100k pedidos de 2016 a 2018.

## Como rodar

**Pré-requisitos:** Docker e Docker Compose instalados.

```bash
git clone https://github.com/leonardomtorres/Olist-pipeline.git
cd Olist-pipeline

# configure as variáveis de ambiente
cp .env.example .env

# sobe o banco
docker compose up db -d

# carrega os dados (coloque os CSVs em data/raw/ antes)
docker compose run --rm pipeline python load_to_postgres.py

# roda as transformações dbt
docker compose run --rm dbt run

# sobe o dashboard
docker compose up dashboard -d
```

Dashboard disponível em `http://localhost:8501`

## Estrutura

```
olist-pipeline/
├── pipeline/        # ingestão dos CSVs
├── dbt/
│   └── models/
│       ├── staging/ # views de limpeza
│       └── mart/    # tabelas analíticas
├── dashboard/       # streamlit
├── db/              # init do postgres
└── .github/         # CI
```

## Modelos dbt

**Staging**
- `stg_orders`, `stg_customers`, `stg_order_items`, `stg_order_payments`, `stg_products`

**Mart**
- `mart_receita_mensal` — receita por mês
- `mart_ticket_por_estado` — ticket médio por estado
- `mart_performance_entrega` — taxa de atraso por estado

## Resultado

- 96.477 pedidos processados
- R$ 15,4 milhões em receita total
- Ticket médio de R$ 190,66
