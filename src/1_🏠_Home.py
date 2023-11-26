import streamlit as st
from Reader import Reader

if __name__ == '__main__':
    st.set_page_config(layout="centered")
    # Create reader object
    filepath = '/Users/seanharris/git/open-data/data/'
    reader = Reader(filepath)

    st.title('Statsbomb data analysis')

    select_comp = reader.load_competition_options()
    comp_option = st.sidebar.selectbox('Please select a competition', (select_comp.keys()))
    comp_id, season_id = select_comp[comp_option]

    select_game = reader.load_match_options(comp_id, season_id)
    game_option = st.sidebar.selectbox('Please select a game', (select_game.keys()))
    match_id = select_game[game_option]['id']
    home = select_game[game_option]['home']
    away = select_game[game_option]['away']
    scoreline = select_game[game_option]['scoreline']

    if st.sidebar.button('Load match') or 'df' not in st.session_state:
        st.session_state.df = reader.load_match_data(match_id)
        st.session_state.home = home
        st.session_state.away = away
        st.session_state.lineups = reader.load_teamsheets(match_id)
        st.session_state.scoreline = scoreline

    st.subheader(st.session_state.scoreline)
    lineup_0, lineup_1 = st.session_state.lineups

    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Home')
        for i, player in lineup_0.iterrows():
            if len(player['positions']) > 0:
                initial = ''
                if player['player_nickname']:
                    for letter in player['player_nickname'].split(' '):
                        initial += letter[0]
                    st.caption(str(player['jersey_number']) + ' ' + player['player_nickname'] + ', ' + initial)
                else:
                    for letter in player['player_name'].split(' '):
                        initial += letter[0]
                    st.caption(str(player['jersey_number']) + ' ' + player['player_name'] + ', ' + initial)

    with col2:
        st.subheader('Away')
        for i, player in lineup_1.iterrows():
            if len(player['positions']) > 0:
                initial = ''
                if player['player_nickname']:
                    for letter in player['player_nickname'].split(' '):
                        initial += letter[0]
                    st.caption(str(player['jersey_number']) + ' ' + player['player_nickname'] + ', ' + initial)
                else:
                    for letter in player['player_name'].split(' '):
                        initial += letter[0]
                    st.caption(str(player['jersey_number']) + ' ' + player['player_name'] + ', ' + initial)