import streamlit as st
import json
import pandas as pd
from statsbombpy import sb

class Reader:

    def __init__(self, filepath=None):
        self.filepath = filepath

    @st.cache_data
    def load_match_data(_self, match_id):
        '''Given a match id returns the event data from that match as a dataframe'''
        if _self.filepath:
            with open(_self.filepath + 'events/' + str(match_id) + '.json') as f:
                game = json.load(f)
            match_df = pd.json_normalize(game, sep='_').assign(match_id=match_id)
        else:
            match_df = sb.events(match_id)
        return match_df

    @st.cache_data
    def load_competition_options(_self):
        '''Returns a dictionary of competitions where the key is a string representation of the competition name and 
        year, and the value is a tuple composed of the competition id and the season id'''
        all_competitions = _self.load_competitions()
        select_comp = {}
        for i, comp in all_competitions.iterrows():
            name = comp['competition_name']
            year = comp['season_name']
            identifier = name + ' ' + year
            select_comp[identifier] = (comp['competition_id'], comp['season_id'])
        return select_comp
    
    @st.cache_data
    def load_competitions(_self):
        '''Returns a dataframe containing the available competitions and their properties'''
        if _self.filepath:
            all_competitions = pd.read_json(_self.filepath + 'competitions.json')
        else:
            all_competitions = sb.competitions()
        return all_competitions
    
    @st.cache_data
    def load_match_options(_self, comp_id, season_id):
        '''Given a competition id and a season id returns a dictionary of matches where the key is the scoreline and the
        value is a dicitonary containing the match_id, home team name, away team name and the scoreline'''
        select_game = {}
        with open(_self.filepath + 'matches/' + str(comp_id) + '/' + str(season_id) + '.json') as f:
            data = json.load(f)
            for i in data:
                scoreline = i['home_team']['home_team_name'] + ' ' + str(i['home_score']) + '-' + str(i['away_score']) + ' ' + i['away_team']['away_team_name']
                select_game[scoreline] = {  "id" : i['match_id'],
                                            "home" : i['home_team']['home_team_name'],
                                            "away" : i['away_team']['away_team_name'],
                                            "scoreline" : scoreline
                                         }
        return select_game

    @st.cache_data
    def load_lineup_data(_self, match_id):
        lineup = []
        with open(_self.filepath + 'lineups/' + str(match_id) + '.json') as f:
            game = json.load(f)
            for x in game:
                temp = pd.json_normalize(x)
                tdf = pd.json_normalize(temp['lineup'][0], sep='_')
                lineup.append(tdf)
        return lineup