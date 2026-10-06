import streamlit as st
import pandas as pd

st.set_page_config(page_title="Visualizador de Dados de impacto da IA em estudantes", layout="wide")
st.title("Visualizador de Dados de impacto da IA em estudantes")

# 1. Cria o botão de upload na tela
arquivo_postado = st.file_uploader("Escolha um arquivo:", type=["csv", "xlsx"])

# O código só roda se o usuário realmente enviar um arquivo
if arquivo_postado is not None:
    
    # 2. Verifica a extensão e lê o arquivo para criar o DataFrame (df)
    if arquivo_postado.name.endswith('.csv'):
        df = pd.read_csv(arquivo_postado)
    else:
        df = pd.read_excel(arquivo_postado)

    # 3. Agora sim, renomeamos as colunas DIRETAMENTE no DataFrame (df)
    df = df.rename(columns={
        'Student_ID': 'Estudante_ID', 
        'Age': 'Idade', 
        'Gender': 'Gênero',
        'Education_Level': 'Nível de Educação', 
        'Daily_Social_Media_Hours': 'Horas de Mídia Social', 
        'Daily_AI_Tool_Usage_Hours': 'Média de Uso de Ferramentas de IA', 
        'Sleep_Hours': 'Horas de Sono',
        'Physical_Activity_Hours': 'Horas de Atividade Física', 
        'Mental_Health_Score': 'Pontuação de Saúde Mental',
        'Physical_Health_Score': 'Pontuação de Saúde Física'
    })

    #Excluindo colunas desnecessárias
    colunas_para_excluir = ['Estudante_ID']
    df = df.drop(columns=colunas_para_excluir)

    # 4. Mostra os dados (dentro do bloco 'if', garantindo que o df existe)
    st.subheader("Visualizando o DataFrame:")
    st.dataframe(df)