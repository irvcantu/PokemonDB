import pandas as pd
import streamlit as st
import streamlit_option_menu
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('https://raw.githubusercontent.com/JustinYSJSU/PokemonDictionary/refs/heads/main/data/pokemonFinal.csv')

df = df.drop(['abilities', 'against_bug', 'against_dark', 'against_dragon',
       'against_electric', 'against_fairy', 'against_fight', 'against_fire',
       'against_flying', 'against_ghost', 'against_grass', 'against_ground',
       'against_ice', 'against_normal', 'against_poison', 'against_psychic',
       'against_rock', 'against_steel', 'against_water', 'japanese_name', 'classfication'], axis=1)

df['is_legendary'] = df['is_legendary'].astype('category')
df['generation'] = df['generation'].astype('category')
df['type1'] = df['type1'].astype('category')
df['type2'] = df['type2'].astype('category')
df['name'] = df['name'].astype('category')

# Background
st.markdown(
    """
    <style>
    .stApp {
        background-color: #181818;
    }
    </style>
    """,
    unsafe_allow_html=True
)
selected = option_menu(
    menu_title=None,
    options=["Home", "Data Analysis", "EDA", "Visualizations"],
    icons=["house", "fire", "globe-americas", "star"],
    menu_icon="pokeball",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#f8f8f8"},
        "icon": {"color": "#ffcc00", "font-size": "24px"},
        "nav-link": {
            "font-size": "20px",
            "text-align": "center",
            "margin": "0px",
            "color": "#333",
            "--hover-color": "#f5f5dc",
            "border-radius": "5px",
            "padding": "5px"
        },
        "nav-link-selected": {"background-color": "#ff4040", "color": "white"},
    }
)

if selected == "Home":
  st.title("Pokemon Database")
  st.subheader("Welcome to the Pokemon Data Analysis App")
  st.write("In this App you will find Pokemon information from Gen 1 to Gen 7")
  image_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/International_Pok%C3%A9mon_logo.svg/1024px-International_Pok%C3%A9mon_logo.svg.png"
  st.image(image_path, use_container_width=True)

  # At end please include your name and an emoji that describe your personality usign caption()
  st.caption("This is a project created by:")
  st.caption("Student :green[Irving Cantú] :sunglasses:")

elif selected == "Data Analysis":
  st.title("Data Overview and Filters")
  # Provide a filter using a selectbox. Please notice that you need to decide which column from your dataset could use as filter.
  Generation = st.selectbox("Select generation", options = ['All', 1, 2, 3, 4, 5, 6, 7])
  if Generation != 'All':
    df = df[df['generation'] == Generation]

  # Add a range filter using a slider. Please notice that you need to decide which column from your dataset could use as range filter.
  base_total_rate = st.slider("Total base range", float(df['base_total'].min()), float(df['base_total'].max()), (float(df['base_total'].min()), float(df['base_total'].max())))
  df = df[(df['base_total'] >= base_total_rate[0]) & (df['base_total'] <= base_total_rate[1])]

  # Use a checkbox to show or hide one of your column from your dataset. Please notice that you need to decide which column from your dataset could use as checkbox.
  is_legendary = st.checkbox("is_legendary")
  if is_legendary:
    df = df[df['is_legendary'] == 1]

  # Display the filtered dataset and a histogram of one column from your dataset.
  st.write("### Filtered Dataset")
  st.dataframe(df)

  fig_e, ax = plt.subplots()
  sns.histplot(df['base_total'], ax=ax)
  st.write("### Histogram of base_total")
  st.pyplot(fig_e)

elif selected == "EDA":
  st.title("Exploratory Data Analysis")
  summary_stats = df.describe()
  st.write("### Summary Statistics")
  st.dataframe(summary_stats)

elif selected == "Visualizations":
  st.title("Visualizations")
  def Fig_1(df):
    fig_1 = px.sunburst(df,
                  path = ['generation', 'is_legendary', 'type1'],
                  values = 'generation')

    st.subheader("Sunburst graph")
    st.write(fig_1)

  def Fig_2(df):
    fig_2 = px.bar_polar(df, r="attack", theta="type1", color="type1",
                      color_discrete_sequence=px.colors.qualitative.Set3)

    st.subheader("Bar Polar")
    st.write(fig_2)

  def Fig_3(df):
    fig_3 = px.box(df, x="generation", y="base_total", color="generation",
                  notched=True, color_discrete_sequence=px.colors.qualitative.Plotly)
    st.subheader("Box plot")
    st.write(fig_3)

  def Fig_4(df):
    fig_4 = px.scatter(
        df,
        x="pokedex_number",
        y="base_total",
        color="generation",
        color_discrete_sequence=px.colors.qualitative.Plotly)

    st.subheader("Scatter graph")
    st.write(fig_4)

  c1, c2 = st.columns(2)
  with c1:
    Fig_1(df)
  with c2:
    Fig_2(df)

  c3, c4 = st.columns(2)
  with c3:
    Fig_3(df)
  with c4:
    Fig_4(df)
