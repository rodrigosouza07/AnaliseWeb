import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Configuração da página (Ícone alterado para um emoji relevante)
st.set_page_config(layout="centered", page_title="Análise de Qualidade de Sono", page_icon='💤')

# --- CONFIGURAÇÃO DA SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Filtros e Opções")
    
    # Exemplo 1: Caixa de seleção para o gênero
    genero = st.multiselect(
        "Selecione o Gênero:",
        options=["Masculino", "Feminino", "Outros"],
        default=["Masculino", "Feminino"]
    )
    
    # Exemplo 2: Slider para intervalo de idade
    idade = st.slider(
        "Selecione a faixa etária:",
        min_value=0, max_value=100, value=(20, 60)
    )
    
    # Exemplo 3: Seletor de período temporal
    periodo = st.date_input(
        "Intervalo de análise:",
        value=[]
    )
    
    st.divider()
    st.caption("Desenvolvido para Análise de Dados de Sono v1.0")

# --- CONTEÚDO PRINCIPAL ---
st.subheader("Análise de Qualidade de Sono")

# O resto do seu código e gráficos entram aqui...
st.write(f"Filtrando dados para idades entre {idade[0]} e {idade[1]} anos.")
