import streamlit as sl
import pandas as pd
import plotly.express as px
import re
from datetime import datetime
import numpy as np



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

    time = sl.selectbox("select the time you want to record your mood", ("1st Time", "2nd Time", "3rd Time"))
    match = re.search(r'\d+', time)
    time_num = int(match.group(0))
    mood_val = df.loc[df["time"] == time_num]["mood"].squeeze()
    timestamp = df.loc[df["time"] == time_num]["timestamp"].squeeze()

    print(mood_val)

    if np.isnan(mood_val):
        new_mood_val = sl.text_input("How'd your mood today?")
        if new_mood_val:
            new_mood_val = float(new_mood_val)
            now = datetime.now()
            formatted_time = now.strftime("%I:%M %p")
            print(formatted_time)
            df.at[time_num - 1, "timestamp"] = formatted_time
            df.at[time_num - 1, "mood"] = new_mood_val
            df.to_csv(day_file, index=False)
    else:
        sl.write(f"Your mood was already recorded on ***{timestamp}*** and your mood was ***{mood_val}***")
