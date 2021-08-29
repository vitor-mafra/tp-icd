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