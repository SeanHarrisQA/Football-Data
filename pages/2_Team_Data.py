import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import json
from pandas.io.json import json_normalize
import streamlit as st

@st.cache_data
def load_match_data():
    with open('../open-data/data/events/3857261.json') as f:
        wal_eng = json.load(f)
    we = pd.json_normalize(wal_eng, sep='_').assign(match_id="3857261")
    return we

st.header('Team analysis')

with st.sidebar:
    team = st.sidebar.radio("Select a team", ('Both', 'Wales', 'England'))