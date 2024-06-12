import streamlit as sl
import pandas as pd
import plotly.express as px


# Added title, radio buttons
sl.title("Mood Recording And Charting App")
type_data = sl.radio("Select what you want to do.", ('View', 'Add'))

if type_data == "View":
    # Added selectbox and read the csv data
    day = sl.selectbox("Select date to view", ("Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"))
    day_file = day.lower().replace(" ", "")
    df = pd.read_csv(f"{day_file}.csv")

    # Created chart of previous mood ratings
    figure = px.line(x=df.timestamp, y=df.mood, labels={'x': "Time", 'y': "Mood Rating"})
    sl.plotly_chart(figure)
elif type_data == "Add":
    day = sl.selectbox("select the day you want to record your mood",
                       ("Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"))
    day = day.lower().replace(" ", "")
    day_file = f"{day}.csv"
    df = pd.read_csv(day_file)