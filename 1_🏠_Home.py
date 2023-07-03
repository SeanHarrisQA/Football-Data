import streamlit as st
import pandas as pd
import json

# Set the layout as wide(This can only be called once per app)
# st.set_page_config(layout="wide")
filepath = '../../Python Learning/open-data/data/'

# Helper methods
@st.cache_data
def load_match_data(match_id):
    with open(filepath + '/events/' + str(match_id) + '.json') as f:
         game = json.load(f)
    match_df = pd.json_normalize(game, sep='_').assign(match_id=match_id)
    home_team, away_team = match_df['team_name'].unique()
    print(home_team, away_team)
    return match_df, away_team, home_team

all_competitions = pd.read_json(filepath + 'competitions.json')

select_comp = {}
for i, comp in all_competitions.iterrows():
        name = comp['competition_name']
        year = comp['season_name']
        identifier = name + ' ' + year
        select_comp[identifier] = (comp['competition_id'], comp['season_id'])
        print(identifier)
        print(select_comp[identifier])

st.title('Statsbomb data analysis')

comp_option = st.selectbox('Please select a competition', (select_comp.keys()))

comp_id, season_id = select_comp[comp_option]
print(type(comp_id))

select_game = {}
with open(filepath + '/matches/' + str(comp_id) + '/' + str(season_id) + '.json') as f:
    data = json.load(f)
    for i in data:
        scoreline = i['home_team']['home_team_name'] + ' ' + str(i['home_score']) + '-' + str(i['away_score']) + ' ' + i['away_team']['away_team_name']
        select_game[scoreline] = i['match_id']

game_option = st.selectbox('Please select a game', (select_game.keys()))

match_id = select_game[game_option]

st.write(match_id)

match_df, away_team, home_team = load_match_data(match_id)

st.write(away_team + ' vs ' + home_team)
st.session_state.df = match_df
st.session_state.home = home_team
st.session_state.away = away_team

st.dataframe(st.session_state.df)


