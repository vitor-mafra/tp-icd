import streamlit as st
import numpy as np
#import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as ss
import seaborn as sns

import plotly as plt
import plotly.express as px
import json
from urllib.request import urlopen
import time
from PIL import Image

st.set_page_config(page_title="Forest Fires in Brazil")
progress_bar = st.progress(0)
st.title("Forest Fires in Brazil")

DATA_URL = ("https://raw.githubusercontent.com/userhv/Forest-Fires-in-Brazil/main/database/incendiosflorestais_focoscalor_estados.csv")

# o dataframe originalmente usado no jupyter notebook 
df = pd.read_csv("https://raw.githubusercontent.com/userhv/Forest-Fires-in-Brazil/main/database/incendiosflorestais_focoscalor_estados.csv",sep="\t", encoding="ISO-8859-1")
area_estado = pd.read_csv("https://raw.githubusercontent.com/userhv/Forest-Fires-in-Brazil/main/database/Area_Plantada_Estado.csv", sep=";")

def load_data(nrows):
    data = pd.read_csv(DATA_URL, encoding='ISO-8859-1', nrows=nrows)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Carregando os dados...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Carregando os dados... Pronto!')
progress_bar.progress(10)

with urlopen("https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson") as response:
    Brazil = json.load(response) # Javascrip object notation 

state_id_map = {}
for feature in Brazil ["features"]:
    feature["id"] = feature["properties"]["name"]
    state_id_map[feature["properties"]["sigla"]] = feature["id"]

plotting_state = st.text("Gerando os gráficos...")
group_info = st.text("")
intro_title = st.markdown("")
intro_text = st.markdown("")

fig1_title = st.markdown("")
fig1 = px.choropleth_mapbox(
    df,
    locations = "Estado",
    geojson = Brazil, #shape information
    color = "Número",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name = "Estado", #the information in the box
    hover_data = ["Número"],
    center={"lat" : -15.793889, "lon" : -47.882778}, # centers in Brazil
    zoom=2.2,
    opacity=0.8,
    animation_frame = "Ano", #creating the application based on the year
    title = "Número de ocorrências de queimadas registradas no Brasil (1998-2017)", 

)

fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.update_geos(fitbounds = "locations", visible = False)
st.write(fig1)

group_info.text("Helio Victor Flexa dos Santos - 2019006680\nMatheus Prado Miranda - 2019007023\nKaio Lucas de Sá - 2019006850\nVitor de Oliveira Mafra - 2018046831")

intro_title.write("## **Introdução**")
intro_text.write('''
A vegetação brasileira reflete a história do país ao longo de centenas de anos. Da extração do pau-brasil até a expansão da fronteira agrícola as florestas do Brasil podem, de alguma forma, refletir a relação de um povo com o seu país. As questões ambientais preocupam e pautam discussões há algum tempo, tendo ganhado tração ao longo dos últimos anos. O que pretendemos investigar nesse trabalho é, em específico, o problema das queimadas no Brasil por um período de 20 anos (*1997 - 2017*). Ao longo desse trabalho, você encontrará (parte dessa) nossa investigação em busca de respostas para algumas perguntas interessantes.

Em qual estação do ano ocorrem mais incêndios florestais? Estamos mesmo enfrentando um aumento do número de ocorrências de queimadas? Estaria isso relacionado aos períodos de governos presidenciais? Houve uma mudança no foco das queimadas ao longo dos anos? O tipo de produto agrícola cultivado em uma região tem alguma relação com o número de incêndios ocorridos ali? Aplicamos os conceitos aprendidos ao longo da matéria de Introdução a Ciência dos Dados para tentar entender melhor todo esse complexo problema tendo como ponto de partida os dados. É isso que você verá a seguir.\n
''')
progress_bar.progress(20)

fig1_title.write("**Número de ocorrências de queimadas registradas no Brasil (1998-2017)**")

# PERGUNTA 1
st.markdown("## **Em quais estações do ano as queimadas são mais frequentes?**")

st.markdown("Para responder essa pergunta, utilizamos apenas estatísticas básicas, por se tratar de uma base pequena.")
st.markdown("Inicialmente, tratamos a nossa base de dados de modo que ficasse separado as estações do ano desde 1998 até 2017, com isso conseguimos visualizar no gráfico que as estações da primavera e do inverno se destacam dentro as demais por ter um número elevado de queimadas. Evidenciamos isso quando trouxemos a tona a soma de queimadas dessas estações tendo no inverno e primavera, respectivamente, com 238954.85 e 231725.11 queimadas nesses 20 anos. Note que a diferença dessas duas estações para as outras duas restantes, verão e outono, é quase duas vezes maior.")
st.markdown("Com isso conseguimos responder que dentre os 20 anos analisados, a estação do ano que possui o maior número de queimdas é o inverno.")

plot_estacoes = Image.open("./plots/queimadas_por_estacao_do_ano.png")
st.image(plot_estacoes, caption="Primavera+Inverno e Outono+Verão formam dois grupos de dados com características parecidas")

hist_primavera_inverno = Image.open("./plots/media_queimadas_inverno_primavera.png")
st.image(hist_primavera_inverno, caption="Apesar da média bastante parecida, a distribuição do número de queimadas segue um pouco diferente")

st.markdown("**Uma simples regressão**")

regressao_inverno = Image.open("./plots/regressao_inverno.png")
st.image(regressao_inverno)

queimadas_por_regiao = Image.open("./plots/queimadas_por_regiao.png")
st.image(queimadas_por_regiao)

st.markdown("**Estatísticas para as queimadas por estação do ano**")

medias_queimadas_estacao = Image.open("./plots/medias_queimadas_estacao.png")
st.image(medias_queimadas_estacao, caption="Médias de queimadas por estação do ano")

queimadas_verao = Image.open("./plots/queimadas_verao.png")
st.image(queimadas_verao)

queimadas_outono = Image.open("./plots/queimadas_outono.png")
st.image(queimadas_outono)

queimadas_inverno = Image.open("./plots/queimadas_inverno.png")
st.image(queimadas_inverno)

queimadas_primavera = Image.open("./plots/queimadas_primavera.png")
st.image(queimadas_primavera)


st.markdown("**Estatísticas para as queimadas por região**")

queimadas_norte = Image.open("./plots/queimadas_norte.png")
st.image(queimadas_norte)

queimadas_nordeste = Image.open("./plots/queimadas_nordeste.png")
st.image(queimadas_nordeste)

queimadas_centro_oeste = Image.open("./plots/queimadas_centro_oeste.png")
st.image(queimadas_centro_oeste)

queimadas_sudeste = Image.open("./plots/queimadas_sudeste.png")
st.image(queimadas_sudeste)

queimadas_sul = Image.open("./plots/queimadas_sul.png")
st.image(queimadas_sul)

# PERGUNTA 2
st.markdown("## **Há um aumento no número de ocorrências com o passar do tempo, e é possível realizar suas previsões por períodos governamentais?**")
st.markdown("Essa pergunta foi abordada, primeiramente, com uma análise exploratória dos dados. Após verificação da base de dados, decidiu-se por escolher um modelo para representação tal que este seja o número total de queimadas por ano, presentes em um novo ‘data frame’(df). Os dados obtidos foram organizados em uma tabela, gráfico de barras, gráfico de linhas e um histograma. Depois, houve uma análise das estatísticas básicas presentes no df, como média, mediana, valores máximo e mínimo, e também a representação dessas em um gráfico de linhas. Além das estatísticas básicas, também examinou-se as medidas de variância e realizou as mesmas interpretações dos indicadores anteriores. Logo após essa exploração inicial dos dados, fez-se necessário uma divisão melhor e por períodos governamentais. Sabendo disso, foram criados 7 novos df’s, a partir do primeiro gerado e com o auxílio da estrutura ‘query’ para seleção desejada, em que cada um continha as informações correspondentes ao período de governo de um específico presidente.\n") 
st.markdown("No entanto, como a base de dados não possuía dados completos para todos os anos de governo de todos os presidentes, alguns df’s acabaram por ficar com um número menor de informações (isso foi verificado e apresentado). Agora, com essa nova separação, começou-se à fazer testes de hipóteses. Com isso, primeiramente foi gerado um intervalo de confiança, do número total de queimadas, para aqueles períodos de governo que dispunham de uma quantidade razoável de dados, sendo representados por dados limites inferior e superior. Contudo, como esse primeiro método para obtenção de intervalos de confiança requer um número minimamente razoável de dados, não foi possível realizá-lo para todos os períodos. Para estes outros, foi feito um ‘bootstrap’ para simular amostras e ter um número de dados suficientes para uma boa representação do intervalo desejado. Desse modo, foi possível obter os limites inferiores e superiores para o intervalo de confiança. Além disso, representou-se todas as novas amostras simuladas em um histograma. Por último, houve o início da realização das regressões lineares, com o auxílio da biblioteca “sklearn”. Esse modelo foi escolhido pois é o mais adequado aos dados presentes na base de dados. Primeiro, fez-se uma regressão linear para o número total de queimadas de todos os anos da base, ou seja, um modelo geral de regressão. Além disso, verificou-se o coeficiente de determinação e o erro absoluto médio para averiguar a qualidade do modelo. Ainda nesse caso, foi feito também um gráfico para representar a regressão. Logo após, repetiu-se todo esse processo para todos os governos que apresentavam dados em mais de 1 ano.")

queimadas_hist = Image.open("./plots/queimadas_ao_longo_do_tempo.png")
st.image(queimadas_hist)

queimadas_linhas = Image.open("./plots/queimadas_linhas.png")
st.image(queimadas_linhas)

queimadas_hist2 = Image.open("./plots/queimadas_hist2.png")
st.image(queimadas_hist2)

st.markdown("**Teste de Hipótese**")

fhc1 = Image.open("./plots/fhc1.png")
st.image(fhc1)

temer1 = Image.open("./plots/temer1.png")
st.image(temer1)

dilma2 = Image.open("./plots/dilma2.png")
st.image(dilma2)

st.markdown("**Regressões Lineares**")

regressao_geral = Image.open("./plots/regressao_geral.png")
st.image(regressao_geral)

regressao_lula1 = Image.open("./plots/regressao_lula1.png")
st.image(regressao_lula1)

regressao_lula2 = Image.open("./plots/regressao_lula2.png")
st.image(regressao_lula2)

regressao_dilma1 = Image.open("./plots/regressao_dilma1.png")
st.image(regressao_dilma1)

regressao_dilma2 = Image.open("./plots/regressao_dilma2.png")
st.image(regressao_dilma2)

st.markdown("Agora, os dados serão relacionados com os fatos históricos mais notáveis que ocorreram no país durante os períodos retratados. Evidentemente, a quantidade de queimadas, uma questão bastante multifatorial, não se deve à apenas resoluções do governo federal e presidência. No entanto, será colocado um principal fato de cada governo que, de forma razoável e interessante, auxilie na análise de verificação dos impactos nesse valor. No governo de Fernando Henrique Cardoso, em 1998, foi assinado um veto ao artigo que proibia queimadas na Lei de Crimes Contra o Meio Ambiente, aprovada durante o seu próprio governo. Com isso, percebe-se o aumento imediato, devido ao incentivo gerado pelo veto, no número de queimadas já em 1999, mantendo-se em uma crescente taxa até o fim de seu segundo mandato. \n") 
st.markdown("Com o início do governo de Lula, essa quantidade de queimadas atingiu o valor recorde. No entanto, os valores começaram a diminuir a cada ano seguinte durante seus dois mandatos devido à criação do Plano de Prevenção e Controle do Desmatamento na Amazônia Legal, que auxiliou na queda dos valores na principal área de foco até então. Já no período de governo de Dilma Rousseff, percebe-se outro aumento considerável das queimadas. Isso é explicado, especialmente, pelo corte de gastos realizados na prevenção e combate ao desmatamento, tal como cortes consideráveis no plano citado e apresentado durante o governo Lula. A queda de 72% desses gastos, portanto, é possivelmente o principal motivo para os níveis mais altos de quantidade de queimadas durante todo o seu período na presidência. Por último, no único ano de governo de Michel Temer presente nos dados, verifica-se uma grande diminuição em relação aos dois anos anteriores. A principal medida que levou à isso, ao contrário de incentivos propostos pelo governo à criação de áreas para mineração, é a recomposição do orçamento do Ibama com recursos do Fundo Amazônia e outras organizações que auxiliam na prevenção do desmatamento, o que permitiu a retomada da fiscalização já no ano de 2017.")

# PERGUNTA 3
st.markdown("## **Houve uma mudança no foco das queimadas ao longo dos anos?**")

df_norte = df.query("Estado == 'Acre' or Estado == 'Amapá' or Estado == 'Amazonas' or Estado == 'Pará' or Estado == 'Rondônia' or Estado == 'Roraima' or Estado == 'Tocantins'")
df_centro_oeste = df.query("Estado == 'Goiás' or Estado == 'Mato Grosso' or Estado == 'Mato Grosso do Sul' or Estado == 'Distrito Federal'")
df_nordeste = df.query("Estado == 'Alagoas' or Estado == 'Bahia' or Estado == 'Ceará' or Estado == 'Maranhão' or Estado == 'Paraíba' or Estado == 'Pernambuco' or Estado == 'Piauí' or Estado == 'Rio Grande do Norte' or Estado == 'Sergipe'")
df_sudeste = df.query("Estado == 'Espírito Santo' or Estado == 'Minas Gerais' or Estado == 'Rio de Janeiro' or Estado == 'São Paulo'")
df_sul = df.query("Estado == 'Paraná' or Estado == 'Rio Grande do Sul' or Estado == 'Santa Catarina'")

# NORTE
fig_norte_title = st.markdown("")
fig_norte = px.choropleth_mapbox(
    df_norte,
    locations = "Estado",
    geojson = Brazil, #shape information
    color = "Número",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name = "Estado", #the information in the box
    hover_data = ["Número"],
    center={"lat" : -3.966559, "lon" : -57.385635}, # centers in norte
    zoom=3.2,
    opacity=0.8,
    animation_frame = "Ano", #creating the application based on the year

)

progress_bar.progress(30)


fig_norte.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_norte.update_geos(fitbounds = "locations", visible = False)
st.write(fig_norte)
fig_norte_title.write("**Número de ocorrências de queimadas registradas na região Norte do Brasil (1998-2017)**")


# NORDESTE
fig_nordeste_title = st.markdown("")
fig_nordeste = px.choropleth_mapbox(
    df_nordeste,
    locations = "Estado",
    geojson = Brazil, #shape information
    color = "Número",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name = "Estado", #the information in the box
    hover_data = ["Número"],
    center={"lat" : -8.384370, "lon" : -40.888867}, # centers in nordeste
    zoom=3.3,
    opacity=0.8,
    animation_frame = "Ano", #creating the application based on the year

)

progress_bar.progress(40)

fig_nordeste.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_nordeste.update_geos(fitbounds = "locations", visible = False)
st.write(fig_nordeste)
fig_nordeste_title.write("**Número de ocorrências de queimadas registradas na região Nordeste do Brasil (1998-2017)**")



# CENTRO-OESTE
fig_centro_oeste_title = st.markdown("")
fig_centro_oeste = px.choropleth_mapbox(
    df_centro_oeste,
    locations = "Estado",
    geojson = Brazil, #shape information
    color = "Número",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name = "Estado", #the information in the box
    hover_data = ["Número"],
    center={"lat" : -15.319302, "lon" : -52.978053}, # centers in centro-oeste
    zoom=3.4,
    opacity=0.8,
    animation_frame = "Ano", #creating the application based on the year

)

progress_bar.progress(50)

fig_centro_oeste.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_centro_oeste.update_geos(fitbounds = "locations", visible = False)
st.write(fig_centro_oeste)
fig_centro_oeste_title.write("**Número de ocorrências de queimadas registradas na região Centro-Oeste do Brasil (1998-2017)**")


# SUDESTE
fig_sudeste_title = st.markdown("")
fig_sudeste = px.choropleth_mapbox(
    df_sudeste,
    locations = "Estado",
    geojson = Brazil, #shape information
    color = "Número",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name = "Estado", #the information in the box
    hover_data = ["Número"],
    center={"lat" :-19.420684, "lon" : -44.867503}, # centers in nordeste
    zoom=3.7,
    opacity=0.8,
    animation_frame = "Ano", #creating the application based on the year

)

progress_bar.progress(60)

fig_sudeste.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_sudeste.update_geos(fitbounds = "locations", visible = False)
st.write(fig_sudeste)
fig_sudeste_title.write("**Número de ocorrências de queimadas registradas na região Sudeste do Brasil (1998-2017)**")


# SUL
fig_sul_title = st.markdown("")
fig_sul = px.choropleth_mapbox(
    df_sul,
    locations = "Estado",
    geojson = Brazil, #shape information
    color = "Número",
    color_continuous_scale="Viridis",
    mapbox_style="carto-positron",
    hover_name = "Estado", #the information in the box
    hover_data = ["Número"],
    center={"lat" : -27.549380, "lon" : -51.459026}, # centers in nordeste
    zoom=3.8,
    opacity=0.8,
    animation_frame = "Ano", #creating the application based on the year

)

progress_bar.progress(80)

fig_sul.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig_sul.update_geos(fitbounds = "locations", visible = False)
st.write(fig_sul)
fig_sul_title.write("**Número de ocorrências de queimadas registradas na região Sul do Brasil (1998-2017)**")

plotting_state.text("Gerando os gráficos... Pronto!")
data_load_state.text("")
plotting_state.text("")
progress_bar.progress(100)
time.sleep(3)
progress_bar.empty()