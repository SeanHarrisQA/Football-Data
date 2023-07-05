import streamlit as st
import pandas as pd
import json

filepath = '../../Python Learning/open-data/data/'

# Helper methods
@st.cache_data
def load_match_data(match_id):
    with open(filepath + '/events/' + str(match_id) + '.json') as f:
         game = json.load(f)
    match_df = pd.json_normalize(game, sep='_').assign(match_id=match_id)
    home_team, away_team = match_df['team_name'].unique()
    return match_df, away_team, home_team

@st.cache_data
def load_competition_data():
    all_competitions = pd.read_json(filepath + 'competitions.json')
    select_comp = {}
    for i, comp in all_competitions.iterrows():
        name = comp['competition_name']
        year = comp['season_name']
        identifier = name + ' ' + year
        select_comp[identifier] = (comp['competition_id'], comp['season_id'])
    return select_comp

@st.cache_data
def load_event_data(comp_id, season_id):
    select_game = {}
    with open(filepath + '/matches/' + str(comp_id) + '/' + str(season_id) + '.json') as f:
        data = json.load(f)
        for i in data:
            scoreline = i['home_team']['home_team_name'] + ' ' + str(i['home_score']) + '-' + str(i['away_score']) + ' ' + i['away_team']['away_team_name']
            select_game[scoreline] = i['match_id']
    return select_game

@st.cache_data
def load_lineup_data(match_id):
    lineup = []
    # pd.read_json(filepath + '/lineups/' + str(match_id) + '.json')
    with open(filepath + '/lineups/' + str(match_id) + '.json') as f:
         game = json.load(f)
         for x in game:
             temp = pd.json_normalize(x)
             tdf = pd.json_normalize(temp['lineup'][0], sep='_')
             lineup.append(tdf)
             #st.dataframe(tdf)
            #  for y in temp['lineup'][0]:
            #      print(y)
            #      tdf = pd.json_normalize(y, sep='_')
                 #st.dataframe(tdf)
             #temp_lineup = temp['lineup'][0][0]['player_name']
             #print("temp['lineup'][0]['player_name']")
             #print(temp_lineup)
    #lineup_df = pd.json_normalize(game, sep='_').assign(match_id=match_id)
    #print(type(lineup_df))
    return lineup


st.title('Statsbomb data analysis')

select_comp = load_competition_data()
comp_option = st.sidebar.selectbox('Please select a competition', (select_comp.keys()))
comp_id, season_id = select_comp[comp_option]

select_game = load_event_data(comp_id, season_id)
game_option = st.sidebar.selectbox('Please select a game', (select_game.keys()))
match_id = select_game[game_option]

if st.sidebar.button('Load match') or 'df' not in st.session_state:
    st.session_state.df, st.session_state.home, st.session_state.away = load_match_data(match_id)
    st.session_state.lineups = load_lineup_data(match_id)
    for lineup in st.session_state.lineups:
        st.dataframe(lineup)
st.write(st.session_state.home + ' vs ' + st.session_state.away)

st.dataframe(st.session_state.df)