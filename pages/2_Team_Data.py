import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import streamlit as st
from MyFCPython import createPitchEdit

if 'df' in st.session_state:
    game, home_team, away_team = st.session_state.df, st.session_state.home, st.session_state.away
else:
    st.warning('Please return to the home page and select a match')

# Variables used throughout the script
pitch_width = 120
pitch_height = 80

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

# Main code
st.title('Team analysis')
st.divider()

game, home_team, away_team = st.session_state.df, st.session_state.home, st.session_state.away

with st.sidebar:
    team = st.sidebar.radio("Select a team", ('Both', home_team, away_team))

# Average positions
fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')
fig.set_facecolor('black')

if team == 'Both' or team == home_team:
    bool = (game['team_name'] == home_team) & (game['period'] == 1) & (game['player_name'].notnull()) & (game['location'].notnull())
    home_actions = game[bool]
    home_players = home_actions['player_name'].unique()

    # Adding the average positions for england (home team)
    for player in home_players:
        avg_x, avg_y = calc_avg_pos(home_actions, player)
        player_pos = plt.Circle((avg_x, avg_y), 2, facecolor='red', edgecolor='white')
        player_pos.set_alpha(.6)
        ax.add_patch(player_pos)
        initial = ''
        for letter in player.split(' '):
            initial += letter[0]
            plt.text(x=avg_x+1.5, y=avg_y+1.5, s=initial, color='white')

if team == 'Both' or team == away_team:
    bool = (game['team_name'] == away_team) & (game['period'] == 1) & (game['player_name'].notnull()) & (game['location'].notnull())
    away_actions = game[bool]
    away_players = away_actions['player_name'].unique()

    # Adding the average positions for wales (home team)
    for player in away_players:
        avg_x, avg_y = calc_avg_pos(away_actions, player)
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

st.subheader('Average Positions')
st.pyplot(fig)
st.divider()

if team == 'Both' or team == home_team:
    # Calculate heatmap as normal
    heats = np.zeros((121,81), int)
    bool = (game['team_name'] == home_team) & (game['location'].notnull())
    player_touches = game[bool]

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

    st.subheader(home_team + ' Heatmap')
    st.pyplot(fig)
    st.caption('Direction of play from left to right')
    st.divider()


if team == 'Both' or team == away_team:
    # Calculate heatmap as normal
    heats = np.zeros((121,81), int)
    bool = (game['team_name'] == away_team) & (game['location'].notnull())
    player_touches = game[bool]

    for i, touch in player_touches.iterrows():
        x = pitch_width - np.round(touch['location'][0]).astype(int)
        y = pitch_height - np.round(touch['location'][1]).astype(int)
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

    st.subheader(away_team + ' Heatmap')
    st.pyplot(fig)
    st.caption('Direction of play from right to left')
    st.divider()

fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')
fig.set_facecolor('black')

shots = game[game.type_name == 'Shot'].set_index('id')

for i, shot in shots.iterrows():
    x = shot['location'][0]
    y = shot['location'][1]
    
    goal = shot['shot_outcome_name']=='Goal'
    team_name = shot['team_name'].strip()
    in_game = shot['period'] != 5
    
    circle_size = 2
    circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 15)

    if team_name == home_team and team != away_team:
        if goal:
            shot_circle = plt.Circle((x, pitch_height-y), circle_size, color='darkorange')
            shot_circle.set_alpha(.9)
            ax.add_patch(shot_circle)
        else:
            shot_circle = plt.Circle((x, pitch_height-y), circle_size, color='darkorange')
            shot_circle.set_alpha(.4)
            ax.add_patch(shot_circle)
    elif team_name == away_team and team != home_team:
        if goal:
            shot_circle = plt.Circle((pitch_width-x, y), circle_size, color='mediumorchid')
            shot_circle.set_alpha(.9)
            ax.add_patch(shot_circle)
        else:
            shot_circle = plt.Circle((pitch_width-x, y), circle_size, color='mediumorchid')
            shot_circle.set_alpha(.4)
            ax.add_patch(shot_circle)
    
plt.text(5, 75, away_team + ' shots', color='mediumorchid')
plt.text(80, 75, home_team + ' shots', color='darkorange')
st.subheader('Shot Map')
fig.set_size_inches(10, 7)

st.pyplot(fig)

st.divider()