import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px


st.title("Traspaso de estudiantes")
st.markdown("This app is a streamlit example only for educational porpouse")

import pydeck 
import pandas as pd
import os
os.environ["MAPBOX_API_KEY"] = 'pk.eyJ1IjoiZGlhemNlc2FyIiwiYSI6ImNrYjlsdXpiNzBmbHYycHVmYXA4cmluOWwifQ.FU1OiMHvPSqVvTsatlaFcA'
DATA_URL = "gps_data.csv"
DOWNTOWN_BOUNDING_BOX = [
    -122.43135291617365,
    37.766492914983864,
    -122.38706428091974,
    37.80583561830737,
]


def in_bounding_box(point):
    lng, lat = point
    in_lng_bounds = DOWNTOWN_BOUNDING_BOX[0] <= lng <= DOWNTOWN_BOUNDING_BOX[2]
    in_lat_bounds = DOWNTOWN_BOUNDING_BOX[1] <= lat <= DOWNTOWN_BOUNDING_BOX[3]
    return in_lng_bounds and in_lat_bounds


df = pd.read_csv(DATA_URL)
# Filter to bounding box

df=df[df['LAT_DESTINO']<-33]

st.write(df)
df=df[df['NUM_EST']<23]
num_est=st.slider("Cantidad de estudiantes traspasados entre colegios",1,30)
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

arc_layer = pydeck.Layer(
    "ArcLayer",
    data=df.query("NUM_EST >= @num_est"),
    get_width="NUM_EST * 2",
    get_source_position=["LON_ORIGEN", "LAT_ORIGEN"],
    get_target_position=["LON_DESTINO", "LAT_DESTINO"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pydeck.ViewState(latitude=-33.4372, longitude=-70.6506, bearing=90, pitch=85, zoom=8,)


TOOLTIP_TEXT = {"html": " {NUM_EST} Estudiantes se cambiaron  de <br /> {NOM_ORIGEN} <br />  a <br /> {NOM_DESTINO} "}
r = pydeck.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
st.write(r)
r.to_html("arc_layer.html", notebook_display=False)
