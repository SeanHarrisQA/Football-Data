from Reader import Reader
import streamlit as st

st.title("Development Playground")

st.caption("A useful space to experiement with new features")

''' Anthing below here is not currently part of the main app '''

filepath = '/Users/seanharris/git/open-data/data/'
reader = Reader(filepath)
comp_id = 11
season_id = 27

st.header('load_match_options result')
result = reader.load_match_options(comp_id, season_id)
st.write(result)

st.header('load_matches result')
result = reader.load_matches(comp_id, season_id)
st.write(result)



