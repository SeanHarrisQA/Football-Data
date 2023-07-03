import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import streamlit as st

if 'df' in st.session_state:
    game = st.session_state.df
    players = game['player_name'].dropna().unique()
else:
    st.warning('Please return to the home page and select a match')

with st.sidebar:
    player = st.sidebar.radio("Select a team", (players))

st.title('Player analysis')

# Variables used throughout the script
pitch_width = 120
pitch_height = 80

# Start of page
st.subheader(player)
st.divider()

# Pass map for given player
st.subheader('Pass Map')
# Select rows all the rows where the given player makes a pass
bool = (game['player_name'] == player) & (game['type_name'] == 'Pass')
passes_1st = game.loc[bool, ['pass_length', 'pass_angle', 'pass_end_location', 'location', 'player_name', 'pass_body_part_name']]
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
    plt.arrow(x_start, y_start, x_end-x_start, y_end - y_start, color='mediumorchid', head_width=1.5, head_length=2, length_includes_head=True)
# Show the plot on the page
fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
st.pyplot(fig)
st.caption('Direction of play from left to right')
st.divider()

# Heatmap for a given player
st.subheader('Heat Map')
# Initalise heats - N.B the way the pitch heights are initialised means there is no need to flip the coordinates
# in the y-axis as with other functions
heats = np.zeros((121,81), int)
# Drop unnecessary rows
bool = (game['player_name'] == player) & (game['location'].notnull()) #& (game['period'] == 1)
player_touches = game[bool]
# Iterate through the rows and calculate the location of every touch
for i, touch in player_touches.iterrows():
    x = np.round(touch['location'][0]).astype(int)
    y = np.round(touch['location'][1]).astype(int)
    # heats[x-3:x+4, y-3:y+4] += 3
    # heats[x-1:x+2, y-1:y+2] += 6
    heats[x-3:x+4, y-1:y+2] += 3
    heats[x-1:x+2, y-3:y+4] += 3
    heats[x-2:x+3, y-2:y+3] += 3
    heats[x-2:x+3, y] += 1
    heats[y, x-2:x+3] += 1
    heats[x-1:x+2, y-1:y+2] +=1
    heats[x,y] +=1

# Plot heatmap
fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'white')
fig.set_facecolor('black')
plt.imshow(np.transpose(heats), cmap='magma')
st.pyplot(fig)
st.caption('Direction of play from left to right')
st.divider()