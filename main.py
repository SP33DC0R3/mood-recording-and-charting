import streamlit as sl
import pandas as pd
import plotly.express as px
import re
from datetime import datetime
import numpy as np



# Added title, radio buttons
sl.title("Mood Recording And Charting App")
type_data = sl.radio("Select what you want to do.", ('View Previous Mood Charts', 'Record Mood Data'))

if type_data == "View Previous Mood Charts":
    # Added selectbox and read the csv data
    day = sl.selectbox("Select date to view", ("Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"))
    day_file = day.lower().replace(" ", "")
    df = pd.read_csv(f"{day_file}.csv")

    # Created chart of previous mood ratings
    figure = px.line(x=df.timestamp, y=df.mood, labels={'x': "Time", 'y': "Mood Rating"})
    sl.plotly_chart(figure)
elif type_data == "Record Mood Data":
    type_add = sl.radio("Select what you want to do.", ('Record New Mood Data', 'Add Previously Recorded Data'))

    if type_add == 'Record New Mood Data':
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
            new_mood_val = sl.text_input("How's your mood today?")
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
    elif type_add == 'Add Previously Recorded Data':
        day = sl.selectbox("Select the day you want to recorded your mood",
                           ("Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"))
        day = day.lower().replace(" ", "")
        day_file = f"{day}.csv"
        df = pd.read_csv(day_file)

        time = sl.selectbox("Select the timestamp you recorded your mood", ("1st Time", "2nd Time", "3rd Time"))
        match = re.search(r'\d+', time)
        time_num = int(match.group(0))
        mood_val = df.loc[df["time"] == time_num]["mood"].squeeze()
        timestamp = df.loc[df["time"] == time_num]["timestamp"].squeeze()

        if np.isnan(mood_val):
            new_mood_val = sl.text_input("How's your mood today?")
            new_time = sl.text_input(r"Enter time in HH\:MM AM/PM", placeholder="Enter the time you recorded your mood.")
            if new_mood_val:
                if new_time:
                    new_mood_val = float(new_mood_val)
                    new_time = new_time.upper()
                    df.at[time_num - 1, "timestamp"] = new_time
                    df.at[time_num - 1, "mood"] = new_mood_val
                    df.to_csv(day_file, index=False)
        else:
            sl.write(f"Your mood was already recorded on ***{timestamp}*** and your mood was ***{mood_val}***")