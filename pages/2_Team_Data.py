import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import json
from pandas.io.json import json_normalize
import streamlit as st
from MyFCPython import createPitchEdit

filepath = '../../Python Learning/open-data/data/events/3857261.json'

# Variables used throughout the script
pitch_width = 120
pitch_height = 80

# Helper methods
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

st.caption('Average Positions')
st.pyplot(fig)

if team == 'Both' or team == 'England':
    # Calculate heatmap as normal
    heats = np.zeros((121,81), int)
    bool = (we['team_name'] == 'England') & (we['location'].notnull())
    player_touches = we[bool]

    for i, touch in player_touches.iterrows():
        x = np.round(touch['location'][0]).astype(int)
        y = np.round(touch['location'][1]).astype(int)
        heats[x, y] += 9
    
    # Lines across the pitch
    heats[:19, 1:19] = np.sum(heats[:19, 1:19])
    heats[:19, 19:31] = np.sum(heats[:19, 19:31])
    heats[:19, 31:51] = np.sum(heats[:19, 31:51])
    heats[:19, 51:63] = np.sum(heats[:19, 51:63])
    heats[:19, 63:81] = np.sum(heats[:19, 63:81])

    heats[19:40, 1:19] = np.sum(heats[19:40, 1:19])
    heats[19:40, 19:31] = np.sum(heats[19:40, 19:31])
    heats[19:40, 31:51] = np.sum(heats[19:40, 31:51])
    heats[19:40, 51:63] = np.sum(heats[19:40, 51:63])
    heats[19:40, 63:81] = np.sum(heats[19:40, 63:81])

    heats[40:61, 1:19] = np.sum(heats[40:61, 1:19])
    heats[40:61, 19:31] = np.sum(heats[40:61, 19:31])
    heats[40:61, 31:51] = np.sum(heats[40:61, 31:51])
    heats[40:61, 51:63] = np.sum(heats[40:61, 51:63])
    heats[40:61, 63:81] = np.sum(heats[40:61, 63:81])

    heats[61:82, 1:19] = np.sum(heats[61:82, 1:19])
    heats[61:82, 19:31] = np.sum(heats[61:82, 19:31])
    heats[61:82, 31:51] = np.sum(heats[61:82, 31:51])
    heats[61:82, 51:63] = np.sum(heats[61:82, 51:63])
    heats[61:82, 63:81] = np.sum(heats[61:82, 63:81])

    heats[82:103, 1:19] = np.sum(heats[82:103, 1:19])
    heats[82:103, 19:31] = np.sum(heats[82:103, 19:31])
    heats[82:103, 31:51] = np.sum(heats[82:103, 31:51])
    heats[82:103, 51:63] = np.sum(heats[82:103, 51:63])
    heats[82:103, 63:81] = np.sum(heats[82:103, 63:81])

    heats[103:121, 1:19] = np.sum(heats[103:121, 1:19])
    heats[103:121, 19:31] = np.sum(heats[103:121, 19:31])
    heats[103:121, 31:51] = np.sum(heats[103:121, 31:51])
    heats[103:121, 51:63] = np.sum(heats[103:121, 51:63])
    heats[103:121, 63:81] = np.sum(heats[103:121, 63:81])

    fig, ax = createPitchEdit(pitch_width, pitch_height, 'yards', 'gray')
    fig.set_facecolor('black')

    plt.imshow(np.transpose(heats), cmap='magma')
    plt.colorbar( fraction=0.03, pad=0.03)

    st.caption('England Heatmap')
    st.pyplot(fig)


if team == 'Both' or team == 'Wales':
    # Calculate heatmap as normal
    heats = np.zeros((121,81), int)
    bool = (we['team_name'] == 'Wales') & (we['location'].notnull())
    player_touches = we[bool]

    for i, touch in player_touches.iterrows():
        x = pitch_width - np.round(touch['location'][0]).astype(int)
        y = pitch_height - np.round(touch['location'][1]).astype(int)
        print(x, y)
        heats[x, y] += 9
    
    # Lines across the pitch
    heats[:19, 1:19] = np.sum(heats[:19, 1:19])
    heats[:19, 19:31] = np.sum(heats[:19, 19:31])
    heats[:19, 31:51] = np.sum(heats[:19, 31:51])
    heats[:19, 51:63] = np.sum(heats[:19, 51:63])
    heats[:19, 63:81] = np.sum(heats[:19, 63:81])

    heats[19:40, 1:19] = np.sum(heats[19:40, 1:19])
    heats[19:40, 19:31] = np.sum(heats[19:40, 19:31])
    heats[19:40, 31:51] = np.sum(heats[19:40, 31:51])
    heats[19:40, 51:63] = np.sum(heats[19:40, 51:63])
    heats[19:40, 63:81] = np.sum(heats[19:40, 63:81])

    heats[40:61, 1:19] = np.sum(heats[40:61, 1:19])
    heats[40:61, 19:31] = np.sum(heats[40:61, 19:31])
    heats[40:61, 31:51] = np.sum(heats[40:61, 31:51])
    heats[40:61, 51:63] = np.sum(heats[40:61, 51:63])
    heats[40:61, 63:81] = np.sum(heats[40:61, 63:81])

    heats[61:82, 1:19] = np.sum(heats[61:82, 1:19])
    heats[61:82, 19:31] = np.sum(heats[61:82, 19:31])
    heats[61:82, 31:51] = np.sum(heats[61:82, 31:51])
    heats[61:82, 51:63] = np.sum(heats[61:82, 51:63])
    heats[61:82, 63:81] = np.sum(heats[61:82, 63:81])

    heats[82:103, 1:19] = np.sum(heats[82:103, 1:19])
    heats[82:103, 19:31] = np.sum(heats[82:103, 19:31])
    heats[82:103, 31:51] = np.sum(heats[82:103, 31:51])
    heats[82:103, 51:63] = np.sum(heats[82:103, 51:63])
    heats[82:103, 63:81] = np.sum(heats[82:103, 63:81])

    heats[103:120, 1:19] = np.sum(heats[103:120, 1:19])
    heats[103:120, 19:31] = np.sum(heats[103:120, 19:31])
    heats[103:120, 31:51] = np.sum(heats[103:120, 31:51])
    heats[103:120, 51:63] = np.sum(heats[103:120, 51:63])
    heats[103:120, 63:81] = np.sum(heats[103:120, 63:81])

    fig, ax = createPitchEdit(pitch_width, pitch_height, 'yards', 'gray')
    fig.set_facecolor('black')

    plt.imshow(np.transpose(heats), cmap='magma')
    plt.colorbar(fraction=0.03, pad=0.03)

    st.caption('Wales Heatmap')
    st.pyplot(fig)