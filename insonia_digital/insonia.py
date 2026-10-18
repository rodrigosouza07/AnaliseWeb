import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

# Configuração da página para aproveitar o espaço máximo da tela
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
    'caffeine_intake_mg': 'Consumo_Cafeina_Mg', # Corrigido: 'caffeine_intake_mg' com dois 'f's conforme o arquivo original
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
    
    # Traduz os valores categóricos dentro das colunas antes de renomear as colunas
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
        st.caption("Dashboard Corrigido v4.3")

# --- CONTEÚDO PRINCIPAL ---
st.title("📊 Painel Avançado de Análise do Sono")

if df is not None:
    # --- APLICANDO OS FILTROS NO DATAFRAME ---
    # Corrigido para extrair o intervalo mínimo e máximo da tupla do slider de idade
    df_filtrado = df[
        (df['Genero'].isin(generos_sel)) &
        (df['Idade'].between(idade_sel[0], idade_sel[1])) &
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
        latencia_media = df_filtrado['Tempo_Ate_Pegar_No_Sono_Min'].mean() if not df_filtrado.empty else 0
        st.metric("Média para Pegar no Sono", f"{latencia_media:.1f} min")
        
    st.divider()
    
    if not df_filtrado.empty:
        # --- LINHA 1 DE GRÁFICOS ---
        g1, g2 = st.columns(2)
        
        with g1:
            st.write("### ☕ Cafeína vs. Eficiência de Sono")
            
            # Plot dos pontos de dispersão interativos
            pontos = alt.Chart(df_filtrado).encode(
                x=alt.X('Consumo_Cafeina_Mg:Q', title='Consumo de Cafeína (mg)'),
                y=alt.Y('Eficiencia_Sono_Pct:Q', title='Eficiência do Sono (%)', scale=alt.Scale(domain=[50, 100]))
            ).mark_circle(size=60, color='#D2691E', opacity=0.6).encode(
                tooltip=['ID_Usuario', 'Idade', 'Consumo_Cafeina_Mg', 'Eficiencia_Sono_Pct']
            )
            
            # Cálculo estável da linha de tendência em Python puro
            if len(df_filtrado) > 1 and df_filtrado['Consumo_Cafeina_Mg'].nunique() > 1:
                m, b = np.polyfit(df_filtrado['Consumo_Cafeina_Mg'], df_filtrado['Eficiencia_Sono_Pct'], 1)
                x_min, x_max = df_filtrado['Consumo_Cafeina_Mg'].min(), df_filtrado['Consumo_Cafeina_Mg'].max()
                df_linha = pd.DataFrame({
                    'Consumo_Cafeina_Mg': [x_min, x_max],
                    'Eficiencia_Sono_Pct': [m * x_min + b, m * x_max + b]
                })
                linha_tendencia = alt.Chart(df_linha).mark_line(color='red', size=3).encode(
                    x='Consumo_Cafeina_Mg:Q',
                    y='Eficiencia_Sono_Pct:Q'
                )
                grafico_cafeina = (pontos + linha_tendencia).properties(height=350).interactive()
            else:
                grafico_cafeina = pontos.properties(height=350).interactive()
                
            st.altair_chart(grafico_cafeina, use_container_width=True)
            
        with g2:
            st.write("### 💼 Eficiência Média do Sono por Profissão")
            grafico_profissao = alt.Chart(df_filtrado).mark_bar(color='#4E79A7', height=20).encode(
                x=alt.X('mean(Eficiencia_Sono_Pct):Q', title='Eficiência Média (%)', scale=alt.Scale(domain=[50, 100])),
                y=alt.Y('Profissao:N', title='Profissão', sort='-x'),
                tooltip=[alt.Tooltip('mean(Eficiencia_Sono_Pct):Q', title='Eficiência Média', format='.1f')]
            ).properties(height=350)
            
            st.altair_chart(grafico_profissao, use_container_width=True)
            
        st.divider()
        
        # --- LINHA 2 DE GRÁFICOS ---
        g3, g4 = st.columns(2)
        
        with g3:
            st.write("### 📱 Tempo de Tela vs. Tempo para Pegar no Sono")
            grafico_tela = alt.Chart(df_filtrado).mark_circle(size=60, opacity=0.6).encode(
                x=alt.X('Tempo_Tela_Antes_Dormir_Min:Q', title='Tempo de Tela Antes de Dormir (min)'),
                y=alt.Y('Tempo_Ate_Pegar_No_Sono_Min:Q', title='Tempo até Pegar no Sono (min)'),
                color=alt.Color('Cronotipo:N', title='Cronotipo'),
                tooltip=['ID_Usuario', 'Tempo_Tela_Antes_Dormir_Min', 'Tempo_Ate_Pegar_No_Sono_Min', 'Cronotipo']
            ).properties(height=350).interactive()
            
            st.altair_chart(grafico_tela, use_container_width=True)
            
        with g4:
            st.write("### 📦 Eficiência de Sono por Categoria de Dívida de Sono")
            grafico_boxplot = alt.Chart(df_filtrado).mark_boxplot(extent='min-max', size=40).encode(
                x=alt.X('Divida_Sono_Categoria:N', title='Categoria de Dívida de Sono', sort=['Sem Dívida', 'Leve', 'Moderada', 'Grave']),
                y=alt.Y('Eficiencia_Sono_Pct:Q', title='Eficiência do Sono (%)', scale=alt.Scale(domain=[50, 100])),
                color=alt.Color('Divida_Sono_Categoria:N', legend=None)
            ).properties(height=350)
            
            st.altair_chart(grafico_boxplot, use_container_width=True)
            
    else:
        st.warning("⚠️ Nenhuma informação foi encontrada para a combinação de filtros selecionada na barra lateral.")
else:
    st.info("💡 Pronto! Agora basta ir na barra lateral e arrastar seu arquivo CSV para gerar o dashboard interativo em Altair.")
