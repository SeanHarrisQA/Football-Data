import streamlit as st
import json
import pandas as pd
from statsbombpy import sb

class Reader:

    def __init__(self, filepath=None):
        self.filepath = filepath
        self.id = hash(filepath)

    @st.cache_data(show_spinner=False)
    def load_match_data(_self, match_id):
        '''Given a match id returns the event data from that match as a dataframe'''
        if _self.filepath:
            with open(_self.filepath + 'events/' + str(match_id) + '.json') as f:
                game = json.load(f)
            match_df = pd.json_normalize(game, sep='_').assign(match_id=match_id)
        else:
            match_df = sb.events(match_id)
        return match_df

    @st.cache_data(show_spinner=False)
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
    
    @st.cache_data(show_spinner=False)
    def load_competitions(_self):
        '''Returns a dataframe containing the available competitions and their properties'''
        if _self.filepath:
            all_competitions = pd.read_json(_self.filepath + 'competitions.json')
        else:
            all_competitions = sb.competitions()
        return all_competitions
    
    @st.cache_data(show_spinner=False)
    def load_match_options(_self, comp_id, season_id):
        '''Given a competition id and a season id returns a dictionary of matches where the key is the scoreline and the
        value is a dicitonary containing the match_id, home team name, away team name and the scoreline'''
        match_options = {}
        all_matches = _self.load_matches(comp_id, season_id)
        for i, row in all_matches.iterrows():
            scoreline = row['home_team_home_team_name'] + ' ' + str(row['home_score']) + '-' + str(row['away_score']) + ' ' + row['away_team_away_team_name']
            match_options[scoreline] = {    "id" : row['match_id'],
                                            "home" : row['home_team_home_team_name'],
                                            "away" : row['away_team_away_team_name'],
                                            "scoreline" : scoreline
                                        }
        return match_options
    
    @st.cache_data(show_spinner=False)
    def load_matches(_self, comp_id, season_id):
        '''Given a competition and a season, return a dataframe where each row corresponds to a match in that season's competition'''
        if _self.filepath:
            with open(_self.filepath + 'matches/' + str(comp_id) + '/' + str(season_id) + '.json') as f:
                all_matches = json.load(f)
                all_matches = pd.json_normalize(all_matches, sep='_')
        else:
            all_matches = sb.matches(competition_id=11, season_id=season_id)
        return all_matches

    @st.cache_data(show_spinner=False)
    def load_teamsheets(_self, match_id):
        '''Loads the lineup dataframe and splits it into two seperate dataframes, one for each team'''
        teamsheets = []
        lineup = _self.load_lineup(match_id)
        for i, row in lineup.iterrows():
            teamsheets.append(pd.json_normalize(row['lineup']))
        return teamsheets
    
    @st.cache_data(show_spinner=False)
    def load_lineup(_self, match_id):
        '''Returns the statsbomb lineup data as a dataframe'''
        if _self.filepath:
            with open(_self.filepath + '/lineups/' + str(match_id) + '.json') as f:
                    game = json.load(f)
                    game = pd.json_normalize(game)
        else:
            game = sb.lineups(match_id=match_id)
        return game
    
    @st.cache_data(show_spinner=False)
    def load_season_actions(_self, matches, player_id):
        progress_text = "Loading season actions. Please wait."
        my_bar = st.progress(0, text=progress_text)
        iteration_prcnt = 100 // len(matches)
        progress = 0
        season_actions = pd.DataFrame()
        for i, match in matches.iterrows():
            # Load match
            event = _self.load_match_data(match['match_id'])
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