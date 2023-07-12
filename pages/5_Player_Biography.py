from statsbombpy import sb
import streamlit as st
import pandas as pd
import numpy as np
import json
from FCPython import createPitch
import matplotlib.pyplot as plt
from MyFCPython import createHalf
from Statsbomb_Position import Statsbomb_Position

# 
import matplotlib as mpl
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
# 

st.set_page_config(layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

@st.cache_data
def load_competitions(local):
    if local:
        all_competitions = pd.read_json(filepath + 'competitions.json')
    else:
        all_competitions = sb.competitions()
    return all_competitions

@st.cache_data
def load_matches(local, season_id):
    if local:
        with open(filepath + '/matches/11/' + str(season_id) + '.json') as f:
            all_matches = json.load(f)
            all_matches = pd.json_normalize(all_matches, sep='_')
    else:
        all_matches = sb.matches(competition_id=11, season_id=season_id)
    return all_matches

@st.cache_data
def load_event(local, match_id):
    if local:
        with open(filepath + '/events/' + str(match_id) + '.json') as f:
            event = json.load(f)
            event = pd.json_normalize(event, sep='_')
    else:
        event = sb.events(match_id=match_id)
    return event

@st.cache_data
def load_lineup(local, match_id):
    if local:
        with open(filepath + '/lineups/' + str(match_id) + '.json') as f:
            game = json.load(f)
            game = pd.json_normalize(game)
    else:
        game = sb.lineups(match_id=match_id)
    return game

@st.cache_data(show_spinner=False)
def load_season_actions(local, matches):
    progress_text = "Loading season actions. Please wait."
    my_bar = st.progress(0, text=progress_text)
    iteration_prcnt = 100 // len(all_matches)
    progress = 0
    season_actions = pd.DataFrame()
    for i, match in all_matches.iterrows():
        # Load match
        event = load_event(local, match['match_id'])
        # Take all the events that involved that player
        bool = (event['player_id'] == player_id) | (event['pass_recipient_id'] == player_id)
        actions = event[bool]
        season_actions = pd.concat([season_actions, actions])
        progress+=iteration_prcnt
        my_bar.progress(progress, text=progress_text)
    my_bar.progress(100, text='Data successfully loaded')
    my_bar.empty()
    season_actions.reset_index(drop=True, inplace=True)
    return season_actions

def draw_shotmap(shots):
    fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')
    fig.set_facecolor('black')

    for i, shot in shots.iterrows():
        x = shot['location'][0]
        y = shot['location'][1]
    
        goal = shot['shot_outcome_name']=='Goal'
        
        circle_size = 2
        circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 15)

        if goal:
            shot_circle = plt.Circle((x, pitch_height-y), circle_size, color='darkorange')
            shot_circle.set_alpha(.9)
            ax.add_patch(shot_circle)
        else:
            shot_circle = plt.Circle((x, pitch_height-y), circle_size, edgecolor='gray')
            shot_circle.set_alpha(.4)
            ax.add_patch(shot_circle)

    # Draw the shotmaps
    st.subheader('Shot Map')
    fig.set_size_inches(10, 7)
    st.pyplot(fig)
    st.divider()

@st.cache_data
def draw_shotmap_half_pitch(shots):
    fig, ax = createHalf(pitch_width, pitch_height, 'yards', 'gray')
    fig.patch.set_alpha(0)

    total_distance = 0

    for i, shot in shots.iterrows():
        prev_x = shot['location'][0]
        prev_y = shot['location'][1]

        total_distance += (120 - prev_x)

        x = prev_y
        y = 60 - (120 - prev_x)
    
        goal = shot['shot_outcome_name']=='Goal'
        
        circle_size = np.sqrt(shot['shot_statsbomb_xg'] * 10)

        if goal:
            shot_circle = plt.Circle((x, y), circle_size, color='darkorange')
            shot_circle.set_alpha(.7)
            ax.add_patch(shot_circle)
        else:
            shot_circle = plt.Circle((x, y), circle_size, edgecolor='gray')
            shot_circle.set_alpha(.4)
            ax.add_patch(shot_circle)

    average_distance = np.round(total_distance / len(season_shots), 2)
    plt.plot([9,9], [60, 60-average_distance], color='gray')
    plt.text(9, 60-average_distance-5, 'Average\ndistance\n' + str(average_distance) + ' yards', horizontalalignment='center',verticalalignment='center', color='grey')

    # Draw the shotmaps
    st.subheader('Shot Map')
    fig.set_size_inches(10, 7)
    st.pyplot(fig)

@st.cache_data
def draw_heatmap_half_pitch(passes):
    fig, ax = createHalf(pitch_width, pitch_height, 'yards', 'gray')
    fig.patch.set_alpha(0)

def calculate_most_common_positions(games):
    all_positions = [0 for x in range(26)]
    for i, match in games.iterrows():
        lineups = load_lineup(True, match['match_id'])
        lineups = lineups[lineups['team_name'] == 'Barcelona']

        event = load_event(True, match['match_id'])
        event = event.iloc[len(event) - 1]
        final_min, final_sec = int(event['minute']), int(event['second'])

        for i, lineup in lineups.iterrows():
            for x in lineup['lineup']:
                if x['player_id'] == player_id:
                    for y in x['positions']:
                        position_id = y['position_id']
                        start_min, start_sec = y['from'].split(':')
                        start_min, start_sec = int(start_min), int(start_sec)
                        if y['to']:
                            end_min, end_sec = y['to'].split(':')
                            end_min, end_sec = int(end_min), int(end_sec)
                        else:
                            end_min, end_sec = final_min, final_sec
                        all_positions[position_id] += 60 * (end_min - start_min) + (end_sec - start_sec)
    draw_positions_by_minutes(all_positions)

def draw_positions_by_minutes(positions):
    statsbomb_positions = get_all_statsbomb_positions()

    fig, ax = createPitch(pitch_width, pitch_height, 'yards', 'gray')
    fig.patch.set_alpha(0)

    viridis = mpl.colormaps['plasma'].resampled(8)
    total_minutes = sum(positions)
    position_strings = ['' for x in range(len(positions) + 1)]
    for i in range(len(positions)):
       position_strings[i] = str(np.round((positions[i] / total_minutes) * 100, 2)) + '%'
       positions[i] = positions[i] / total_minutes
    m = max(positions)
    for i in range(len(positions)):
       positions[i] /= m
    for i in range(1, len(statsbomb_positions)):
        x = statsbomb_positions[i].location[0]
        y = statsbomb_positions[i].location[1]
        s = statsbomb_positions[i].abbrv
        # c = viridis(positions[i])
        plt.text(x, y, s, color='whitesmoke', ha='center', va='bottom', family='fantasy')
        plt.text(x, y, position_strings[i], color='whitesmoke', ha='center', va='top', fontsize='xx-small', family='fantasy')
    st.pyplot(fig)
            
def get_all_statsbomb_positions():
    statsbomb_positions = []

    x = [12, 28, 45, 60, 75, 92, 108]
    y = [10, 25, 40, 55, 70]
    statsbomb_positions.append(Statsbomb_Position('Dummy', [0,0]))
    statsbomb_positions.append(Statsbomb_Position('GK', [x[0], y[2]]))
    statsbomb_positions.append(Statsbomb_Position('RB', [x[1], y[0]]))
    statsbomb_positions.append(Statsbomb_Position('RCB', [x[1], y[1]]))
    statsbomb_positions.append(Statsbomb_Position('CB', [x[1], y[2]]))
    statsbomb_positions.append(Statsbomb_Position('LCB', [x[1], y[3]]))
    statsbomb_positions.append(Statsbomb_Position('LB', [x[1], y[4]]))
    statsbomb_positions.append(Statsbomb_Position('RWB', [x[2], y[0]]))
    statsbomb_positions.append(Statsbomb_Position('RDM', [x[2], y[1]]))
    statsbomb_positions.append(Statsbomb_Position('CDM', [x[2], y[2]]))
    statsbomb_positions.append(Statsbomb_Position('LDM', [x[2], y[3]]))
    statsbomb_positions.append(Statsbomb_Position('LWB', [x[2], y[4]]))
    statsbomb_positions.append(Statsbomb_Position('RM', [x[3], y[0]]))
    statsbomb_positions.append(Statsbomb_Position('RCM', [x[3], y[1]]))
    statsbomb_positions.append(Statsbomb_Position('CM', [x[3], y[2]]))
    statsbomb_positions.append(Statsbomb_Position('LCM', [x[3], y[3]]))
    statsbomb_positions.append(Statsbomb_Position('LM', [x[3], y[4]]))
    statsbomb_positions.append(Statsbomb_Position('RW', [x[4], y[0]]))
    statsbomb_positions.append(Statsbomb_Position('RAM', [x[4], y[1]]))
    statsbomb_positions.append(Statsbomb_Position('CAM', [x[4], y[2]]))
    statsbomb_positions.append(Statsbomb_Position('LAM', [x[4], y[3]]))
    statsbomb_positions.append(Statsbomb_Position('LW', [x[4], y[4]]))
    statsbomb_positions.append(Statsbomb_Position('RCF', [x[6], y[1]]))
    statsbomb_positions.append(Statsbomb_Position('ST', [x[6], y[2]]))
    statsbomb_positions.append(Statsbomb_Position('LCF', [x[6], y[3]]))
    statsbomb_positions.append(Statsbomb_Position('SS', [x[5], y[2]]))
    return statsbomb_positions

st.title('Player Biography')

filepath = '../../Python Learning/open-data/data/'
pitch_width = 120
pitch_height = 80

player_id = 5503

# main script
all_competitions = load_competitions(True)

la_liga = all_competitions[all_competitions['competition_id'] == 11].reset_index(drop=True)

all_seasons = {}

for i, year in la_liga.iterrows():
    all_seasons[year['season_name']] = year['season_id']

season = st.select_slider('Select a season', reversed(all_seasons.keys()))

all_matches = load_matches(True, all_seasons[season])

season_actions = load_season_actions(True, all_matches)

bool = (season_actions['player_id'] == player_id) & (season_actions['type_name'] == 'Shot') & (season_actions['shot_type_id'] != 88)
season_shots = season_actions[bool]

st.subheader("Lionel Messi non-penalty shots " + str(season))

col1, col2 = st.columns([3, 2])

with col1:
    draw_shotmap_half_pitch(season_shots)

with col2:
    goals = len(season_shots[season_shots['shot_outcome_name'] == 'Goal'])
    shots = len(season_shots)
    xG = np.around(season_shots['shot_statsbomb_xg'].sum(), 2)
    xG_per_shot = np.around((xG / shots), 3)
    st.subheader('Stats')
    colA, colB = st.columns(2)
    with colA:
        st.write("Shots: " + str(shots))
        st.write("Goals: " + str(goals))
    with colB:
        st.write("xG: " + str(xG))
        st.write("xG per shot: " + str(xG_per_shot))

    # Tally shots for each time
    piechart_values = season_shots['shot_body_part_name'].value_counts()
    inner_values = []
    for body_part in piechart_values.index:
        bool = (season_shots['shot_body_part_name'] == body_part) & (season_shots['shot_outcome_name'] == 'Goal')
        no_of_misses = piechart_values[body_part] - len(season_shots[bool])
        no_of_goals = len(season_shots[bool])
        inner_values.append(no_of_misses)
        inner_values.append(no_of_goals)
        
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    size = 0.3
    fig1, ax1 = plt.subplots()
    fig1.patch.set_alpha(0)
    cmap = plt.get_cmap("tab20c")
    colours = cmap(np.array([4, 12, 0, 16]))
    inner_colours = cmap(np.array([5, 6, 13, 14, 1, 2, 17, 18]))
    test = ["Missed", "Scored", "Missed", "Scored", "Missed", "Scored", "Missed", "Scored"]
    o_patches, o_texts, o_autotexts = ax1.pie(piechart_values, labels=piechart_values.index, colors=colours, autopct='%1.1f%%', wedgeprops=dict(width=size, edgecolor='w'))
    something, qualcosa = ax1.pie(inner_values, radius=1-size, colors=inner_colours, wedgeprops=dict(width=size, edgecolor='w'))
    legend = ax1.legend(something, test, title="Inner Ring",loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), framealpha=0, labelcolor='w')
    plt.setp(legend.get_title(), color='w')
    for text in o_texts:
        text.set_color('darkorange')
    for autotext in o_autotexts:
        autotext.set_color('white')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# calculate_most_common_positions(all_matches)

st.dataframe(season_actions)
draw_heatmap_half_pitch(season_actions)