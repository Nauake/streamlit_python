# # import pandas as pd
# #
# # dados = pd.read_excel("Classificacao_teste.xlsx")
# # # print(dados.head(30))
# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.
#
#
# from dash import Dash, html, dcc
# import plotly.express as px
# import pandas as pd
#
# app = Dash()
#
# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
#
#
# data = {'Materias':["AA TAF", "PISTOLA", "AA TEC MIL I", "AA PATRULHA II"],
#       'Medias':[9.452, 8.187, 8.357, 8.839]
#       }
# df = pd.DataFrame(data)
#
# fig = px.bar(df, x="Materias", y="Medias", barmode="group")
# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
#     html.H2(children="Fatura tudo"),
#
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])
#
# if __name__ == '__main__':
#     app.run(debug=True)
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
dados = pd.read_excel("Classificacao_teste.xlsx")
dados_filtrados = dados[["NOME", "TIRO PISTOLA", "AA PATRULHA II", "AA TAF", "AA TEC MIL I",
                         "MÉDIA DO BÁSICO", "MÉDIA_PARCIAL"]]
dados_filtrados.index.name = "POSIÇÃO"
dados_filtrados.index += 1

nomes = list(dados["NOME"])
nomes.insert(0, "Todos os nomes")

st.header("Notas do Curso de Infantaria")

selec_box = st.sidebar.selectbox(
    "Escolha seu nome:",
    nomes
)
if selec_box == "Todos os nomes":
    tabela = dados_filtrados
    st.table(tabela)
else:
    tabela = dados_filtrados.loc[dados_filtrados["NOME"] == selec_box]
    st.table(tabela)
    # Dados
    materias = ["TIRO PISTOLA", "AA PATRULHA II", "AA TAF", "AA TEC MIL I"]
    # Dados do aluno
    dado_aluno = dados.loc[dados["NOME"] == selec_box, ["TIRO PISTOLA", "AA PATRULHA II",
    "AA TAF", "AA TEC MIL I"]]
    nota_aluno = list(dado_aluno.iloc[0])
    # Dados da Média da materia
    media_materia = [
        round(dados["TIRO PISTOLA"].mean(), 3),
        round(dados["AA PATRULHA II"].mean(), 3),
        round(dados["AA TAF"].mean(), 3),
        round(dados["AA TEC MIL I"].mean(), 3),
    ]

    # Configuração do gráfico com Matplotlib
    x = np.arange(len(materias))  # Posições das barras
    width = 0.4  # Largura das barras

    fig, ax = plt.subplots()
    barra1 = ax.bar(x - width / 2, nota_aluno, width=width, label=selec_box, color='red')
    barra2 = ax.bar(x + width / 2, media_materia, width=width, label='Média da Matéria', color='orange')
    # Informações Adicionais
    ax.set_ylim(0, 12)
    ax.set_xlabel('DISCIPLINAS')
    ax.set_ylabel('NOTAS')
    ax.set_xticks(x)
    ax.set_xticklabels(materias) # Nomes das Notas
    # Valores na barra
    ax.bar_label(barra1, padding=2)
    ax.bar_label(barra2, padding=2)
    ax.legend()
    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)


