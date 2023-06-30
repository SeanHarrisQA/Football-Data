import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import json
from pandas.io.json import json_normalize
import streamlit as st

filepath = '../../Python Learning/open-data/data/events/3857261.json'

# Variables used throughout the script
pitch_width = 120
pitch_height = 80

@st.cache_data
def load_match_data():
    with open(filepath) as f:
        wal_eng = json.load(f)
    we = pd.json_normalize(wal_eng, sep='_').assign(match_id="3857261")
    return we

def calc_avg_pos(df, player):
    # Get all the rows for a given player
    locations = df.loc[df['player_name'] == player, ['location', 'player_name']]
    
    total_x = 0
    total_y = 0
    rows = 0
    for i, event in locations.iterrows():
        x = event['location'][0]
        y = event['location'][1]
        total_x += x
        total_y += y
        rows+=1
    
    average_x = np.round(total_x / rows, 2)
    average_y = np.round(total_y / rows, 2)
    print(f"{player}: ({average_x}, {average_y})")
    adj_y = 80 - average_y
    
    return [average_x, adj_y]

st.header('Team analysis')

we = load_match_data()

with st.sidebar:
    team = st.sidebar.radio("Select a team", ('Both', 'Wales', 'England'))

# Average positions
fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')
fig.set_facecolor('black')

if team == 'Both' or team == 'England':
    bool = (we['team_name'] == 'England') & (we['period'] == 1) & (we['player_name'].notnull()) & (we['location'].notnull())
    eng_actions = we[bool]
    eng_players = eng_actions['player_name'].unique()

    # Adding the average positions for england (home team)
    for player in eng_players:
        avg_x, avg_y = calc_avg_pos(eng_actions, player)
        player_pos = plt.Circle((avg_x, avg_y), 2, facecolor='red', edgecolor='white')
        player_pos.set_alpha(.6)
        ax.add_patch(player_pos)
        initial = ''
        for letter in player.split(' '):
            initial += letter[0]
            plt.text(x=avg_x+1.5, y=avg_y+1.5, s=initial, color='white')

if team == 'Both' or team == 'Wales':
    bool = (we['team_name'] == 'Wales') & (we['period'] == 1) & (we['player_name'].notnull()) & (we['location'].notnull())
    wal_actions = we[bool]
    wal_players = wal_actions['player_name'].unique()

    # Adding the average positions for wales (home team)
    for player in wal_players:
        avg_x, avg_y = calc_avg_pos(wal_actions, player)
        # Adjust for away team
        adj_x = pitch_width - avg_x
        adj_y = pitch_height - avg_y
        player_pos = plt.Circle((adj_x, adj_y), 2, facecolor='blue', edgecolor='white')
        player_pos.set_alpha(.6)
        ax.add_patch(player_pos)
        initial = ''
        for letter in player.split(' '):
            initial += letter[0]
            plt.text(x=adj_x+1.5, y=adj_y+1.5, s=initial, color='white')

st.pyplot(fig)