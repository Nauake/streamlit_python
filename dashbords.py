import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px

# Aplicando CSS
with open("style.css") as file:
    st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)

# Pegando os dados e configurando
path = r"Classificacao_Infa.xlsx"
dados = pd.read_excel(path, header=1, usecols=range(8))
dados.index += 1

# Criar um dataframe de um aluno
def dados_aluno(aluno):
    global dados
    aluno_notas = dados[dados['NOME'] == aluno].values[0]
    aluno_notas.tolist()
    # aluno_notas = [4340, 'AUHELBITON', 9.75, 9.297, 9.667, 8.778, 8.509, 9.085]
    # dois ultimos números é MÉDIA DO BÁSICO e MÉDIA PARCIAL
    tabela_aluno = {
        "DISCIPLINA": ["TIRO PISTOLA", "AA PATRULHA II", 
                       "AA TFM II", "AA TEC MIL I"],
        "NOTAS": aluno_notas[2:6] # Notas das disciplinas
    }
    tabela_aluno = pd.DataFrame(tabela_aluno)
    return tabela_aluno

def graf_media_disciplia(aluno, notas_aluno:float, nome_disciplina:str, medias_disciplinas: float):
    # Criar DataFrame para o gráfico
    dados_grafico = pd.DataFrame({
        "Categoria": [aluno, "Média da Disciplina"],
        "Nota": [notas_aluno, medias_disciplinas]
    })
    # Criar gráfico de barras com plotly express
    fig = px.bar(
        dados_grafico,
        x="Categoria",
        y="Nota",
        color="Categoria",
        text="Nota",
        color_discrete_map={
            aluno: "green",
            "MÉDIA DA DISCIPLINA": "blue"
        }
    )
    # Configurando o layout
    #fig.update_layout(title={'x': 0.2}) # centraliza
    fig.update_layout(
        title={'text': f"{nome_disciplina}"},
        yaxis_title_font=dict(color="red", size=16),
        xaxis_title_font=dict(color="blue", size=16),
        xaxis_tickfont=dict(color="black", size=14),
        xaxis_title=None,
        yaxis_title=None,
        showlegend= False

    )
    fig.update_layout(yaxis=dict(range=[0, 11]))  # Ajusta escala de 0 a 10
    fig.update_traces(texttemplate='%{text:.3f}', textposition='outside')

    return fig

# PÁGINAS
escolha = option_menu(
    menu_title=None,
    options=['CLASSIFICAÇÃO GERAL', 'MÉDIA POR DISCIPLINA'],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f0f0f5"},
        "icon": {"color": "orange", "font-size": "18px"}, 
        "nav-link": {
            "border-radius": "15px",
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#4CAF50"}
    }
)

if escolha == "CLASSIFICAÇÃO GERAL":
# PÁGINA PRINCIPAL
    st.header("Tabela de Classificação da Infantaria")
    st.write("---")
    # Opções dos nomes - Select box
    opcoes_nome = dados['NOME'].tolist()
    opcoes_nome.insert(0, "TODOS OS ALUNOS")
    aluno = st.selectbox("Alunos", opcoes_nome)
    # Mostrar a tabela
    if aluno == 'TODOS OS ALUNOS':
        st.write(dados)
    else:
        st.subheader(aluno)
        classif = dados[dados['NOME'] == aluno].index[0]
        st.write(f'##### Classificação na Infantaria: {classif}')
        st.write(dados_aluno(aluno=aluno))
elif escolha == "MÉDIA POR DISCIPLINA":
    # Opções dos nomes - Select box
    opcoes_nome = dados['NOME'].tolist()
    aluno = st.selectbox("Alunos", opcoes_nome)
    # MÉDIA POR DISCIPLIA
    medias_disciplinas = {
        'TIRO PISTOLA':round(float(dados['TIRO PISTOLA'].mean()), 3),
        "AA PATRULHA II": round(float(dados['AA PATRULHA II'].mean()), 3),
        "AA TFM II": round(float(dados['AA TFM II'].mean()), 3),
        "AA TEC MIL I": round(float(dados['AA TEC MIL I'].mean()), 3)
    }
    aluno_notas = dados[dados['NOME'] == aluno].iloc[0].to_dict()
    notas_aluno = {
        'TIRO PISTOLA': aluno_notas['TIRO PISTOLA'],
        "AA PATRULHA II": aluno_notas['AA PATRULHA II'],
        "AA TFM II": aluno_notas['AA TFM II'],
        "AA TEC MIL I": aluno_notas['AA TEC MIL I']
    }
    # Gráficos das Disciplinas
    fig_tiro_pistola = graf_media_disciplia(aluno, notas_aluno["TIRO PISTOLA"], "TIRO PISTOLA", medias_disciplinas["TIRO PISTOLA"])
    fig_patrulha = graf_media_disciplia(aluno, notas_aluno["AA PATRULHA II"], "AA PATRULHA II", medias_disciplinas["AA PATRULHA II"])
    fig_tfm = graf_media_disciplia(aluno, notas_aluno["AA TFM II"], "AA TFM II", medias_disciplinas["AA TFM II"])
    fig_tecmil1 = graf_media_disciplia(aluno, notas_aluno["AA TEC MIL I"], "AA TEC MIL I", medias_disciplinas["AA TEC MIL I"])
    
    # Mostrar os Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_tiro_pistola, use_container_width=True)
        st.plotly_chart(fig_patrulha, use_container_width=True)
    with col2:
        st.plotly_chart(fig_tfm, use_container_width=True)
        st.plotly_chart(fig_tecmil1, use_container_width=True)
    




