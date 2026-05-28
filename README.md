# Olist Data Pipeline

Pipeline de engenharia de dados end-to-end usando o dataset público da Olist (e-commerce brasileiro). O projeto cobre ingestão, transformação e visualização de ~100k pedidos reais.

## Arquitetura

```
CSV (Kaggle)
    │
    ▼
Python + SQLAlchemy  ──►  PostgreSQL (schema: raw)
                                │
                                ▼
                          dbt (staging + mart)
                                │
                          ┌─────┴──────┐
                          ▼            ▼
                    raw_staging    raw_mart
                                        │
                                        ▼
                                  Streamlit Dashboard
```

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Ingestão | Python, pandas, SQLAlchemy |
| Armazenamento | PostgreSQL 15 |
| Transformação | dbt-core |
| Orquestração | Docker Compose |
| Visualização | Streamlit, Plotly |
| CI/CD | GitHub Actions |
| Testes | pytest |

## Dataset

[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — 9 tabelas, ~100k pedidos de 2016 a 2018.

## Como rodar

**Pré-requisitos:** Docker e Docker Compose instalados.

```bash
# Clone o repositório
git clone https://github.com/leonardomtorres/Olist-pipeline.git
cd olist-pipeline

# Configure as variáveis de ambiente
cp .env.example .env

# Suba o banco de dados
docker compose up db -d

# Carregue os dados brutos (coloque os CSVs em data/raw/ primeiro)
docker compose run --rm pipeline python load_to_postgres.py

# Execute as transformações dbt
docker compose run --rm dbt run

# Suba o dashboard
docker compose up dashboard -d
```

Acesse o dashboard em `http://localhost:8501`

## Estrutura do projeto

```
olist-pipeline/
├── pipeline/               # Ingestão: carrega CSVs no PostgreSQL
│   ├── load_to_postgres.py
│   ├── requirements.txt
│   └── Dockerfile
├── dbt/                    # Transformações ELT
│   ├── models/
│   │   ├── staging/        # Views de limpeza e padronização
│   │   └── mart/           # Tabelas analíticas finais
│   ├── dbt_project.yml
│   └── profiles.yml
├── dashboard/              # Visualização com Streamlit
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── db/
│   └── init.sql            # Criação dos schemas
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions
├── docker-compose.yml
└── .env.example
```

## Modelos dbt

**Staging** (views — limpeza e tipagem):
- `stg_orders` — pedidos com datas convertidas
- `stg_customers` — clientes com estado extraído
- `stg_order_items` — itens com preço e frete
- `stg_order_payments` — pagamentos consolidados
- `stg_products` — produtos com categoria traduzida

**Mart** (tabelas — agregações analíticas):
- `mart_receita_mensal` — receita e volume de pedidos por mês
- `mart_ticket_por_estado` — ticket médio por estado
- `mart_performance_entrega` — taxa de atraso por estado

## Dashboard

- Receita total: **R$ 15,4 milhões**
- Total de pedidos: **96.477**
- Ticket médio: **R$ 190,66**
- Gráficos de receita mensal, ticket por estado e performance de entrega
