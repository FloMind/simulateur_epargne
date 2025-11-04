import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Simulateur d'Épargne", layout="wide")

st.title("💰 Simulateur d'Épargne et de Capitalisation")
st.markdown("**Calcule la croissance de ton épargne avec un taux d’intérêt composé.**")
st.divider()

st.sidebar.header("⚙️ Paramètres de simulation")
capital_initial = st.sidebar.number_input("Capital initial (€)", min_value=0, max_value=1_000_000, value=10_000, step=1_000)
versement_mensuel = st.sidebar.number_input("Versement mensuel (€)", min_value=0, max_value=10_000, value=200, step=50)
taux_annuel = st.sidebar.slider("Taux d’intérêt annuel (%)", min_value=0.0, max_value=15.0, value=4.0, step=0.1)
duree = st.sidebar.slider("Durée (années)", min_value=1, max_value=50, value=20)

def simulation(capital_initial, versement_mensuel, taux_annuel, duree):
    capital = capital_initial
    taux_mensuel = taux_annuel / 100 / 12
    data = []
    for mois in range(duree * 12):
        capital = capital * (1 + taux_mensuel) + versement_mensuel
        if mois % 12 == 0:
            data.append({"Année": mois // 12, "Capital (€)": round(capital, 2)})
    return pd.DataFrame(data)

df = simulation(capital_initial, versement_mensuel, taux_annuel, duree)

st.subheader("📈 Résultats de la simulation")
col1, col2 = st.columns(2)
col1.metric(label="Capital final", value=f"{df['Capital (€)'].iloc[-1]:,.0f} €")
col2.metric(label="Durée", value=f"{duree} ans")

fig = px.line(
    df, 
    x="Année", 
    y="Capital (€)", 
    title="Évolution du capital au fil du temps",
    markers=True,
    line_shape="spline"
)
fig.update_layout(
    xaxis_title="Années",
    yaxis_title="Capital (€)",
    template="simple_white",
    title_x=0.3
)
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.caption("Créé avec par **Florent Cochet** | [GitHub](https://github.com/FloMind) | © MindEdge Finance 2025")
