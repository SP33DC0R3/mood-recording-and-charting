import streamlit as sl
import pandas as pd

# Added title, radio buttons
sl.title("Mood Recording And Charting App")
type_data = sl.radio("Select what you want to do.", ('View', 'Add'))