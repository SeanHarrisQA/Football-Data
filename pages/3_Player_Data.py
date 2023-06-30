import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import json
from pandas.io.json import json_normalize
import streamlit as st

filepath = '../../Python Learning/open-data/data/events/3857261.json'

@st.cache_data
def load_match_data():
    with open(filepath) as f:
        wal_eng = json.load(f)
    we = pd.json_normalize(wal_eng, sep='_').assign(match_id="3857261")
    return we

st.header('Player analysis')

# Variables used throughout the script
pitch_width = 120
pitch_height = 80
player = 'Luke Shaw'

# Start of page
st.subheader(player)
we = load_match_data()

# Pass map for given player
st.caption('Pass Map')
# Select rows all the rows where the given player makes a pass
bool = (we['player_name'] == player) & (we['type_name'] == 'Pass')
passes_1st = we.loc[bool, ['pass_length', 'pass_angle', 'pass_end_location', 'location', 'player_name', 'pass_body_part_name']]
# Create plot
fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'white')
fig.set_facecolor('black')
# Plot the passes
for a_pass in passes_1st.iterrows():
    length = a_pass[1][0]
    angle = a_pass[1][1]
    x_end = a_pass[1][2][0] 
    y_end = pitch_height-a_pass[1][2][1]
    x_start = a_pass[1][3][0]
    y_start = pitch_height-a_pass[1][3][1]
    plt.arrow(x_start, y_start, x_end-x_start, y_end - y_start, color='red', head_width=1.5, head_length=2, length_includes_head=True)
# Show the plot on the page
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
st.pyplot(fig)

# Heatmap for a given player
st.caption('Heat Map')
# Initalise heats - N.B the way the pitch heights are initialised means there is no need to flip the coordinates
# in the y-axis as with other functions
heats = np.zeros((121,81), int)
# Drop unnecessary rows
bool = (we['player_name'] == player) & (we['location'].notnull()) & (we['period'] == 1)
player_touches = we[bool]
# Iterate through the rows and calculate the location of every touch
for i, touch in player_touches.iterrows():
    x = np.round(touch['location'][0]).astype(int)
    y = np.round(touch['location'][1]).astype(int)
    heats[x-3:x+4, y-3:y+4] += 3
    heats[x-1:x+2, y-1:y+2] += 6
# Plot heatmap
fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'white')
fig.set_facecolor('black')
plt.imshow(np.transpose(heats), cmap='magma')
st.pyplot(fig)