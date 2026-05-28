import os
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Olist Pipeline", layout="wide")

@st.cache_resource
def get_engine():
    return create_engine(
        "postgresql+psycopg2://",
        connect_args={
            "host": os.getenv("POSTGRES_HOST"),
            "port": int(os.getenv("POSTGRES_PORT")),
            "dbname": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
        }
    )

@st.cache_data
def carregar_dados(query):
    engine = get_engine()
    return pd.read_sql(query, engine)

st.title("Olist — Dashboard de Vendas")
st.markdown("---")

col1, col2, col3 = st.columns(3)

receita = carregar_dados("select * from raw_mart.mart_receita_mensal order by mes")
ticket = carregar_dados("select * from raw_mart.mart_ticket_por_estado order by receita_total desc")
entrega = carregar_dados("select * from raw_mart.mart_performance_entrega order by pct_atraso desc")

with col1:
    st.metric("Total de Pedidos", f"{receita['total_pedidos'].sum():,.0f}")

with col2:
    st.metric("Receita Total", f"R$ {receita['receita_total'].sum():,.2f}")

with col3:
    st.metric("Ticket Médio Geral", f"R$ {ticket['ticket_medio'].mean():,.2f}")

st.markdown("---")

st.subheader("Receita Mensal")
fig1 = px.line(receita, x="mes", y="receita_total", markers=True)
st.plotly_chart(fig1, use_container_width=True)

col4, col5 = st.columns(2)

with col4:
    st.subheader("Ticket Médio por Estado")
    fig2 = px.bar(ticket.head(10), x="estado", y="ticket_medio", color="ticket_medio")
    st.plotly_chart(fig2, use_container_width=True)

with col5:
    st.subheader("Taxa de Atraso por Estado")
    fig3 = px.bar(entrega.head(10), x="estado", y="pct_atraso", color="pct_atraso")
    st.plotly_chart(fig3, use_container_width=True)