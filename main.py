import streamlit as sl
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np
import os
import csv
from functions import *


# Added title, radio buttons
sl.title("Mood Recording And Charting App")
type_data = sl.radio("Select what you want to do.", ('View Previous Mood Charts', 'Record Mood Data'), key="type_data")

csv_format = [
    ["time", "timestamp", "mood"],
    [1, "", ""],
    [2, "", ""],
    [3, "", ""]
]

files = []
if "files" in os.listdir("."):
    for file in os.listdir("./files"):
        files.append(file)
else:
    os.mkdir("files")
    for file in os.listdir("./files"):
        files.append(file)

day_names = []
for file in files:
    day = filename_to_day(file)
    day_names.append(day)

day_names = sorted(day_names, key=custom_sort)

if type_data == "View Previous Mood Charts":
    # Added selectbox and read the csv data
    view_day = sl.selectbox("Select date to view", day_names,
                            key="view_day")
    if view_day:
        day_file = day_to_filename(view_day)
        df = pd.read_csv(f"files/{day_file}")

        # Created chart of previous mood ratings
        figure = px.line(x=df.timestamp, y=df.mood, labels={'x': "Time", 'y': "Mood Rating"})
        sl.plotly_chart(figure)
    else:
        sl.warning("Please create a new day and add data to it")
elif type_data == "Record Mood Data":
    type_add = sl.radio("Select what you want to do.", ('Record New Mood Data', 'Add Previously Recorded Data'),
                        key="type_add")
    new_day_btn = sl.button("Add New Day")
    if new_day_btn:
        try:
            new_day_file = increment_day(day_names[-1])
            new_day_file = day_to_filename(new_day_file)
        except IndexError:
            new_day_file = "day1.csv"
        with open(f"./files/{new_day_file}", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(csv_format)
        sl.rerun()
    if type_add == 'Record New Mood Data':
        new_day = sl.selectbox("Select the day you want to record your mood",
                               day_names, key="new_day")
        if new_day:
            day_file = day_to_filename(new_day)
            df = pd.read_csv(f"files/{day_file}")
            new_time = sl.selectbox("select the time you want to record your mood",
                                    ("1st Record", "2nd Record", "3rd Record"), key='new_time')
            match = re.search(r'\d+', new_time)
            time_num = int(match.group(0))
            mood_val = df.loc[df["time"] == time_num]["mood"].squeeze()
            timestamp = df.loc[df["time"] == time_num]["timestamp"].squeeze()

            if np.isnan(mood_val):
                new_mood_val = sl.text_input("How's your mood today?", key='new_mood_val')
                if sl.button("Save"):
                    if new_mood_val:
                        new_mood_val = float(new_mood_val)
                        now = datetime.now()
                        formatted_time = now.strftime("%I:%M %p")
                        df.at[time_num - 1, "timestamp"] = formatted_time
                        df.at[time_num - 1, "mood"] = new_mood_val
                        df.to_csv(f"./files/{day_file}", index=False)

                        sl.success("Data Saved Successfully")
            else:
                sl.write(f"Your mood was already recorded on ***{timestamp}*** and your mood was ***{mood_val}***")
        else:
            sl.warning("Please create a new day and add data to it")
    elif type_add == 'Add Previously Recorded Data':
        prev_day = sl.selectbox("Select the day you want to recorded your mood",
                                day_names, key='prev_day')
        if prev_day:
            day_file = day_to_filename(prev_day)
            df = pd.read_csv(f"files/{day_file}")

            curr_time = sl.selectbox("Select the timestamp you recorded your mood",
                                     ("1st Record", "2nd Record", "3rd Record"), key='curr_time')
            match = re.search(r'\d+', curr_time)
            time_num = int(match.group(0))
            mood_val = df.loc[df["time"] == time_num]["mood"].squeeze()
            timestamp = df.loc[df["time"] == time_num]["timestamp"].squeeze()

            if np.isnan(mood_val):
                new_mood_val = sl.text_input("How's your mood today?", key='new_mood_val')
                new_time = sl.text_input(r"Enter time in HH\:MM AM/PM",
                                        placeholder="Enter the time you recorded your mood.", key='new_time')
                if sl.button("Save"):
                    if new_mood_val and new_time:
                        new_mood_val = float(new_mood_val)
                        time_obj = datetime.strptime(new_time, "%I:%M %p")
                        formatted_time = time_obj.strftime("%I:%M %p")
                        df.at[time_num - 1, "timestamp"] = formatted_time
                        df.at[time_num - 1, "mood"] = new_mood_val
                        df.to_csv(f"./files/{day_file}", index=False)

                        sl.success("Data Saved Successfully")
                    else:
                        sl.warning("Please fill in both fields to save the data.")
            else:
                sl.write(f"Your mood was already recorded on ***{timestamp}*** and your mood was ***{mood_val}***")
        else:
            sl.warning("Please create a new day and add data to it")