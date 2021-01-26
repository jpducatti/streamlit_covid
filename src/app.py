import streamlit as st
import pandas as  pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

#ao trabalhor com códigos, ao contrário do notebook que lemos de cima pra baixo, cria-se função para tudo de modo a deixar
#claro o que está sendo feito e ORGANIZADO
# função def main() que define a aplicação e faz várias coisas: recebe título, plotagem do dataframe, 

def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados

def grafico_comparativo_2(dados_2019,dados_2020,causa="TODAS",estado="BRASIL"):

    if estado == "BRASIL":
        if causa == "TODAS":
            total_obitos_2019 = dados_2019["total"].sum()
            total_obitos_2020 = dados_2020["total"].sum()
            lista = [int(total_obitos_2019),int(total_obitos_2020)]
        else:
            total_obitos_2019 = dados_2019.groupby("tipo_doenca")["total"].sum()
            total_obitos_2020 = dados_2020.groupby("tipo_doenca")["total"].sum()
            lista = [int(total_obitos_2019.loc[causa]),int(total_obitos_2020.loc[causa])]
    else:
        if causa == "TODAS":
            total_obitos_2019 = dados_2019.groupby("uf")["total"].sum()
            total_obitos_2020 = dados_2020.groupby("uf")["total"].sum()
            lista = [int(total_obitos_2019.loc[estado]),int(total_obitos_2020.loc[estado])]    
        else:
            total_obitos_2019 = dados_2019.groupby(["tipo_doenca","uf"])["total"].sum().unstack().fillna(0).stack()
            total_obitos_2020 = dados_2020.groupby(["tipo_doenca","uf"])["total"].sum().unstack().fillna(0).stack()

            lista = [int(total_obitos_2019.loc[causa,estado]),int(total_obitos_2020.loc[causa,estado])]

    dados = pd.DataFrame({"Total":lista,
                           "Ano":[2019,2020]})

    fig, ax = plt.subplots()
    ax = sns.barplot(x="Ano",y="Total",data=dados)
    ax.set_title(f"Óbitos por {causa} - {estado}")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Óbitos")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))

    
    for p in ax.patches:
        ax.annotate('{:,.0f}'.format(p.get_height()),(p.get_x()+0.4,p.get_height()),ha="center",va="bottom",color="black",                         fontweight="bold")

    return fig #não vamos plotar aqui a figura, apenas retorná-la para renderizar na main

def main():
    
    obitos_2019 = carrega_dados(r"dados\obitos-2019.csv")
    obitos_2020 = carrega_dados(r"dados\obitos-2020.csv")
    
    tipo_doenca = np.append(obitos_2020["tipo_doenca"].unique(),"TODAS")
    estado = np.append(obitos_2020["uf"].unique(),"BRASIL")
    ver_tabela = ["Não","Sim"]
   

    st.title("Análise Óbitos 2019-2020 :man-cartwheeling:")
    st.markdown("Este trabalho analisa dados dos **óbitos 2019-2020**") #**para deixar em negrito/bold
    st.text("Projeto e fontes em: https://github.com/jpducatti/streamlit_covid")
    
    opcao_1 = st.sidebar.selectbox("Selecione o tipo de doença",
                 tipo_doenca)
    opcao_2 = st.sidebar.selectbox("Selecione o estado",
                 estado)
    opcao_3 = st.sidebar.selectbox("Gostaria de ver a base de dados?",
                 ver_tabela)                           
    figura = grafico_comparativo_2(obitos_2019,obitos_2020,
                                   opcao_1,opcao_2)

    st.pyplot(figura) #deixar para o main renderizar o gráfico
    if opcao_3 == "Sim":
       st.text("Tabela de dados 2019")
       st.dataframe(obitos_2019)
       st.text("Tabela de dados 2020")
       st.dataframe(obitos_2020)
    else:
       pass

#indica que o python ao rodar script roda primeira a função main
if __name__ == "__main__":  
    main()



