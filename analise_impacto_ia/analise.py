import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import numpy as np

st.set_page_config(page_title="Visualizador de Dados de impacto da IA em estudantes", layout="wide")
st.title("Visualizador de Dados de impacto da IA em estudantes")

# 1. Cria o botão de upload na tela'
with st.sidebar:
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

    # Indicadores resumidos para uma leitura rápida do conjunto de dados
    st.subheader("Painel de indicadores")
    indicadores = [("Estudantes analisados", f"{len(df)}")]
    indicadores_numericos = [
        ('Idade', "Idade média", " anos"),
        ('Média de Uso de Ferramentas de IA', "Uso médio de IA", " h/dia"),
        ('Horas de Sono', "Sono médio", " h/dia"),
        ('Pontuação de Saúde Mental', "Saúde mental média", ""),
    ]
    for coluna, rotulo, unidade in indicadores_numericos:
        if coluna in df.columns:
            valores = pd.to_numeric(df[coluna], errors='coerce')
            media = valores.mean()
            if pd.notna(media):
                indicadores.append((rotulo, f"{media:.1f}{unidade}"))

    cards = st.columns(len(indicadores))
    for card, (rotulo, valor) in zip(cards, indicadores):
        card.metric(rotulo, valor)

    # Gráficos: uso médio de IA por gênero, relação com idade e nível de
    # escolaridade mais frequente.
    col_genero = 'Gênero'
    col_idade = 'Idade'
    col_uso_ia = 'Média de Uso de Ferramentas de IA'
    col_escolaridade = 'Nível de Educação'

    if all(coluna in df.columns for coluna in [col_genero, col_idade, col_uso_ia, col_escolaridade]):
        dados_graficos = df.copy()
        dados_graficos[col_idade] = pd.to_numeric(dados_graficos[col_idade], errors='coerce')
        dados_graficos[col_uso_ia] = pd.to_numeric(dados_graficos[col_uso_ia], errors='coerce')
        dados_graficos = dados_graficos.dropna(
            subset=[col_genero, col_idade, col_uso_ia, col_escolaridade]
        )

        st.subheader("Análise de idade, uso de IA e escolaridade")
        col_pizza, col_dispersao = st.columns(2)

        uso_medio_genero = dados_graficos.groupby(col_genero)[col_uso_ia].mean().sort_values(ascending=False)
        with col_pizza:
            st.markdown("**Média de uso de ferramentas de IA por gênero**")
            if not uso_medio_genero.empty and uso_medio_genero.sum() > 0:
                # Prepara o DataFrame para o Altair
                df_pizza = uso_medio_genero.reset_index()
                
                grafico_pizza = alt.Chart(df_pizza).mark_arc().encode(
                    theta=alt.Theta(field=col_uso_ia, type="quantitative"),
                    color=alt.Color(field=col_genero, type="nominal", title="Gênero"),
                    tooltip=[
                        alt.Tooltip(field=col_genero, type="nominal", title="Gênero"),
                        alt.Tooltip(field=col_uso_ia, type="quantitative", title="Média (h/dia)", format=".2f")
                    ]
                )
                st.altair_chart(grafico_pizza, use_container_width=True)
            else:
                st.info("Não há dados suficientes para o gráfico de pizza.")

        with col_dispersao:
            st.markdown("**Idade x uso de IA, por gênero**")
            grafico_dispersao = alt.Chart(dados_graficos).mark_circle(size=70).encode(
                x=alt.X(field=col_idade, type="quantitative", title="Idade"),
                y=alt.Y(field=col_uso_ia, type="quantitative", title="Uso de ferramentas de IA (h/dia)"),
                color=alt.Color(field=col_genero, type="nominal", title="Gênero"),
                tooltip=[col_genero, col_idade, col_uso_ia],
            )
            st.altair_chart(grafico_dispersao.interactive(), use_container_width=True)

        frequencia_escolaridade = dados_graficos[col_escolaridade].value_counts()
        st.markdown("**Frequência por nível de escolaridade**")
        st.bar_chart(frequencia_escolaridade)

        nivel_mais_frequente = frequencia_escolaridade.idxmax() if not frequencia_escolaridade.empty else None
        idade_media_genero = dados_graficos.groupby(col_genero)[col_idade].mean()
        if not dados_graficos.empty:
            genero_maior_uso = uso_medio_genero.idxmax()
            resumo_idades = "; ".join(
                f"{genero}: {idade:.1f} anos" for genero, idade in idade_media_genero.items()
            )
            # resumo = (
            #     f"- A maior média de uso de ferramentas de IA é do gênero **{genero_maior_uso}** "
            #     f"({uso_medio_genero[genero_maior_uso]:.1f} horas por dia).\n"
            #     f"- A idade média por gênero é: {resumo_idades}.\n"
            #     f"- O nível de escolaridade mais frequente é **{nivel_mais_frequente}** "
            #     f"({frequencia_escolaridade.iloc[0]} estudantes)."
            # )
            # st.subheader("Resumo dos gráficos")
            # st.markdown(resumo)

        df_resumo = pd.DataFrame({
            "Métrica": [
                "Maior média de uso de IA",
                "Idade média por gênero",
                "Nível de escolaridade mais frequente"
            ],
            "Resumo": [
                f"{genero_maior_uso} ({uso_medio_genero[genero_maior_uso]:.1f} h/dia)",
                resumo_idades,
                f"{nivel_mais_frequente} ({frequencia_escolaridade.iloc[0]} estudantes)"
            ]
        })
        st.subheader("Resumo em tabela")
        st.dataframe(df_resumo, use_container_width=True)

    else:
        st.warning("Não foi possível gerar os gráficos: confira se as colunas de gênero, idade, uso de IA e escolaridade estão disponíveis.")