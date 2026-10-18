import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Configuração da página para aproveitar melhor o espaço da tela
st.set_page_config(layout="wide", page_title="Análise de Qualidade de Sono", page_icon='💤')

# --- DICIONÁRIOS DE TRADUÇÃO ---
TRADUCAO_COLUNAS = {
    'user_id': 'ID_Usuario',
    'age': 'Idade',
    'gender': 'Genero',
    'chronotype': 'Cronotipo',
    'occupation': 'Profissao',
    'bedtime_hour': 'Hora_Ir_Cama',
    'screen_time_before_bed_min': 'Tempo_Tela_Antes_Dormir_Min',
    'primary_app_category': 'Categoria_Principal_App',
    'screen_brightness_pct': 'Brilho_Tela_Pct',
    'blue_light_filter_on': 'Filtro_Luz_Azul_Ativo',
    'caffeine_intake_mg': 'Consumo_Caffeina_Mg',
    'caffeine_last_hour': 'Ultima_Hora_Cafeina',
    'physical_activity_min': 'Atividade_Fisica_Min',
    'room_temperature_f': 'Temperatura_Quarto_F',
    'ambient_noise_db': 'Ruido_Ambiente_Db',
    'sleep_onset_latency_min': 'Tempo_Ate_Pegar_No_Sono_Min',
    'total_sleep_hours': 'Total_Horas_Sono',
    'rem_sleep_pct': 'Sono_REM_Pct',
    'deep_sleep_pct': 'Sono_Profundo_Pct',
    'awakenings_count': 'Numero_Despertares',
    'sleep_efficiency_pct': 'Eficiencia_Sono_Pct',
    'next_day_fatigue_score': 'Pontuacao_Fatiga_Proximo_Dia',
    'sleep_debt_category': 'Divida_Sono_Categoria'
}

MAPEAMENTO_VALORES = {
    'gender': {'Female': 'Feminino', 'Male': 'Masculino', 'Non-Binary': 'Não-Binário'},
    'chronotype': {'Intermediate': 'Intermediário', 'Night Owl': 'Vespertino (Noturno)', 'Early Bird': 'Matutino'},
    'occupation': {'Student': 'Estudante', 'Professional': 'Profissional', 'Retired': 'Aposentado', 'Unemployed': 'Desempregado', 'Freelancer': 'Autônomo'},
    'sleep_debt_category': {'Moderate': 'Moderada', 'No Debt': 'Sem Dívida', 'Mild': 'Leve', 'Severe': 'Grave'}
}

# --- FUNÇÃO PARA CARREGAR E TRADUZIR DADOS ---
@st.cache_data
def carregar_e_traduzir_dados(arquivo):
    df_raw = pd.read_csv(arquivo)
    
    # Traduz os valores categóricos dentro das colunas
    for coluna, mapeamento in MAPEAMENTO_VALORES.items():
        if coluna in df_raw.columns:
            df_raw[coluna] = df_raw[coluna].map(mapeamento).fillna(df_raw[coluna])
            
    # Traduz o nome das colunas
    df_raw = df_raw.rename(columns=TRADUCAO_COLUNAS)
    return df_raw

df = None

# --- SIDEBAR (CONFIGURAÇÕES E FILTROS) ---
with st.sidebar:
    st.header("⚙️ Configurações e Filtros")
    arquivo_postado = st.file_uploader("1. Importe o CSV de Sono:", type=["csv"])
    
    if arquivo_postado is not None:
        df = carregar_e_traduzir_dados(arquivo_postado)
        
        st.divider()
        st.subheader("👥 Filtros Demográficos")
        
        # Filtro de Gênero
        opcoes_genero = df['Genero'].unique().tolist()
        generos_sel = st.multiselect("Gênero:", options=opcoes_genero, default=opcoes_genero)
        
        # Filtro de Idade
        min_idade, max_idade = int(df['Idade'].min()), int(df['Idade'].max())
        idade_sel = st.slider("Faixa Etária:", min_value=min_idade, max_value=max_idade, value=(min_idade, max_idade))
        
        # Filtro de Profissão
        opcoes_prof = df['Profissao'].unique().tolist()
        prof_sel = st.multiselect("Profissão/Ocupação:", options=opcoes_prof, default=opcoes_prof)
        
        st.divider()
        st.subheader("🧬 Perfil Biológico")
        
        # Filtro de Cronotipo
        opcoes_crono = df['Cronotipo'].unique().tolist()
        crono_sel = st.multiselect("Cronotipo:", options=opcoes_crono, default=opcoes_crono)
        
        # Filtro de Luz Azul
        luz_azul = st.radio("Filtro de Luz Azul Celular:", options=["Todos", "Ativado", "Desativado"])
        
        st.divider()
        st.caption("Dashboard de Qualidade de Sono v3.0")

# --- CONTEÚDO PRINCIPAL ---
st.title("📊 Painel Avançado de Análise do Sono")

if df is not None:
    # --- APLICANDO OS FILTROS NO DATAFRAME ---
    df_filtrado = df[
        (df['Genero'].isin(generos_sel)) &
        (df['Idade'].between(idade_sel[0], idades_sel[1] if 'idades_sel' in locals() else idade_sel[1])) &
        (df['Profissao'].isin(prof_sel)) &
        (df['Cronotipo'].isin(crono_sel))
    ]
    
    if luz_azul == "Ativado":
        df_filtrado = df_filtrado[df_filtrado['Filtro_Luz_Azul_Ativo'] == True]
    elif luz_azul == "Desativado":
        df_filtrado = df_filtrado[df_filtrado['Filtro_Luz_Azul_Ativo'] == False]
        
    # --- KPIs NO TOPO ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Amostras Filtradas", len(df_filtrado))
    with col2:
        ef_media = df_filtrado['Eficiencia_Sono_Pct'].mean() if not df_filtrado.empty else 0
        st.metric("Eficiência Média", f"{ef_media:.1f}%")
    with col3:
        horas_medias = df_filtrado['Total_Horas_Sono'].mean() if not df_filtrado.empty else 0
        st.metric("Média de Horas Dormidas", f"{horas_medias:.1f}h")
    with col4:
        cafe_medio = df_filtrado['Consumo_Caffeina_Mg'].mean() if not df_filtrado.empty else 0
        st.metric("Consumo Médio de Cafeína", f"{cafe_medio:.0f} mg")
        
    st.divider()
    
    if not df_filtrado.empty:
        # --- BLOCO DE GRÁFICOS 1 & 2 ---
        g1, g2 = st.columns(2)
        
        with g1:
            st.write("### ☕ Impacto do Consumo de Cafeína na Eficiência")
            fig1, ax1 = plt.subplots(figsize=(6, 4))
            ax1.scatter(df_filtrado['Consumo_Caffeina_Mg'], df_filtrado['Eficiencia_Sono_Pct'], color='#D2691E', alpha=0.5, edgecolors='none')
            
            # Adiciona linha de tendência se houver dados suficientes
            if len(df_filtrado) > 1:
                m, b = np.polyfit(df_filtrado['Consumo_Caffeina_Mg'], df_filtrado['Eficiencia_Sono_Pct'], 1)
                x_vals = np.array([df_filtrado['Consumo_Caffeina_Mg'].min(), df_filtrado['Consumo_Caffeina_Mg'].max()])
                ax1.plot(x_vals, m*x_vals + b, color='red', linestyle='--', linewidth=2, label='Tendência')
            
            ax1.set_xlabel("Cafeína (mg)")
            ax1.set_ylabel("Eficiência do Sono (%)")
            ax1.grid(True, linestyle=':', alpha=0.6)
            fig1.patch.set_facecolor('none')
            ax1.set_facecolor('none')
            st.pyplot(fig1)
            
        with g2:
            st.write("### 💼 Eficiência Média do Sono por Profissão")
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            dados_prof = df_filtrado.groupby('Profissao')['Eficiencia_Sono_Pct'].mean().sort_values()
            
            cores = plt.cm.Blues(np.linspace(0.4, 0.8, len(dados_prof)))
            ax2.barh(dados_prof.index, dados_prof.values, color=cores, height=0.6)
            ax2.set_xlabel("Eficiência Média (%)")
            ax2.set_xlim(0, 100)
            for i, v in enumerate(dados_prof.values):
                ax2.text(v + 1, i, f"{v:.1f}%", va='center', fontweight='bold', fontsize=9)
                
            fig2.patch.set_facecolor('none')
            ax2.set_facecolor('none')
            st.pyplot(fig2)
            
        st.divider()
        
        # --- BLOCO DE GRÁFICOS 3 & TABELA ---
        g3, g4 = st.columns([1, 2])
        
        with g3:
            st.write("### 🕒 Distribuição de Perfil Biológico")
            fig3, ax3 = plt.subplots(figsize=(4, 4))
            dados_crono = df_filtrado['Cronotipo'].value_counts()
            
            ax3.pie(dados_crono.values, labels=dados_crono.index, autopct='%1.1f%%', 
                    startangle=90, colors=['#4E79A7', '#F28E2B', '#E15759'], 
                    textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'w', 'linewidth': 1})
            
            fig3.patch.set_facecolor('none')
            st.pyplot(fig3)
            
        with g4:
            st.write("### 📋 Planilha de Dados Filtrados")
            # Mostra as colunas principais já em português na tabela interativa
            colunas_exibicao = ['ID_Usuario', 'Idade', 'Genero', 'Profissao', 'Cronotipo', 'Total_Horas_Sono', 'Eficiencia_Sono_Pct', 'Divida_Sono_Categoria']
            st.dataframe(df_filtrado[colunas_exibicao].head(10), use_container_width=True)
            
    else:
        st.warning("⚠️ Nenhuma informação foi encontrada para a combinação de filtros selecionada na barra lateral.")
else:
    st.info("💡 Pronto! Agora basta ir na barra lateral e arrastar seu arquivo CSV para gerar o dashboard completo traduzido.")
