import streamlit as st
import altair as alt
import pandas as pd

st.title("My Title")

st.write("# Markdown Title(Hello World)")

"# Markdown Title(Hello World)"

st.write("This is **bold** *italics* and ~~strikethrough~~")

st.write("This is a link [https://app.perusall.com/courses/si-649-001-fa-2021/streamlit-walkthrough]")

# st.write("![alt text][http://]") image

car_url = ""

cars = pd.read_json(car_url)

st.write(cars)

hp_mpg = alt.Chart(cars).mark_circle(size = 80, opacity = 0.5).encode(
    x = 'Horsepower:Q',
    y = 'Miles_per_Gallon:Q',
    color = 'Origin'
)

st.write(hp_mpg)

hp_mpg


#button
btn = st.button("display the hp_mp vis")
if btn:
    hp_mpg
else:
    "click the button to see the vis"


#drop-down box
y_axis_options = ["Acceleration", "Miles_per_Gallon","Displacement"]
y_axis_select = st.selectbox(lab = "Select what you want the y axis to be", options = y_axis_options)

hp_mpg = alt.Chart(cars).mark_circle(size = 80, opacity = 0.5).encode(
    x = 'Horsepower:Q',
    y = y_axis_select,
    color = 'Origin'
)

hp_mpg

st.sidebar.title("Sidebar title")

st.sidebar.write("My sidebar stuff")