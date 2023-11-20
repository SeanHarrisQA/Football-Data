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