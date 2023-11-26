import pandas as pd
import json
import numpy as np
import math
import sys
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import streamlit as st
from MyFCPython import createHalf, create_pitch_scaleable
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier

## Functions for feature design ####################################################################

# Returns the distance in yards from the goalline
def get_x(point):
    return 120 - point[0]

# Returns the distance in yards from the centre line of the pitch (i.e a line 
# from the centre of the goal to the centre of the other goal)
def get_dc(point):
    return abs(40 - point[1])

# Returns the distance in yards from the centre of the goal
def get_distance_from_goal(point):
    xs, ys = point
    xg, yg = [120, 40]
    return np.sqrt((xg-xs)**2 + (yg-ys)**2)

# Returns the angle between the lines from the spot the shot is taken from to each goalpost
def get_angle(point):
    xs, ys = point
    xl, yl = [120, 44]
    xr, yr = [120, 36]
    sr = np.sqrt((xr-xs)**2 + (yr-ys)**2)
    sl = np.sqrt((xl-xs)**2 + (yl-ys)**2)
    cosRSL = (sr**2 + sl**2 - 8**2) / (2 * sr * sl)
    ans = math.degrees(math.atan(cosRSL))
    return ans

def get_blocking_players(arr, location):
    if type(arr) is list:
        opp_count = 0
        # Calculate both lines and make sure the y value is between them, and the x value is to the right of the 
        # shot location
        x1, y1 = location
        x2, y2 = 120, 36
        x3, y3 = 120, 44
        den12 = x2-x1  
        a12 = (y2-y1)/ den12 if den12 != 0 else (y2-y1)/ 0.00001
        b12 = y2 - a12*x2
        den13 = x3-x1
        a13 = (y3-y1)/ den13 if den13 != 0 else (y3-y1)/ 0.00001
        b13 = y3 - a13*x3
        for i in range(len(arr)):
            if arr[i]['teammate'] == False:
                xo, yo = arr[i]['location']
                if xo > x1 and yo > a12*xo + b12 and yo < a13*xo + b13:
                    opp_count += 1
        return opp_count
    else:
        return 0
    
def get_blocking_players_include_team(arr, location):
    if type(arr) is list:
        opp_count = 0
        # Calculate both lines and make sure the y value is between them, and the x value is to the right of the 
        # shot location
        x1, y1 = location
        x2, y2 = 120, 36
        x3, y3 = 120, 44
        den12 = x2-x1  
        a12 = (y2-y1)/ den12 if den12 != 0 else (y2-y1)/ 0.00001
        b12 = y2 - a12*x2
        den13 = x3-x1
        a13 = (y3-y1)/ den13 if den13 != 0 else (y3-y1)/ 0.00001
        b13 = y3 - a13*x3
        for i in range(len(arr)):
            xo, yo = arr[i]['location']
            if xo > x1 and yo > a12*xo + b12 and yo < a13*xo + b13:
                opp_count += 1
        return opp_count
    else:
        return 0
    
def goal_yes_no(outcome):
    if outcome =='Goal':
        return 1
    else:
        return 0
    
## Functions for loading data ######################################################################

filepath = '/Users/seanharris/git/open-data/data/'

def load_competition_data():
    all_competitions = pd.read_json(filepath + 'competitions.json')
    return all_competitions

def load_event_data(comp_id, season_id):
    with open(filepath + '/matches/' + str(comp_id) + '/' + str(season_id) + '.json') as f:
        data = json.load(f)
    return data

def load_match_data(match_id):
    with open(filepath + '/events/' + str(match_id) + '.json') as f:
         game = json.load(f)
    match_df = pd.json_normalize(game, sep='_').assign(match_id=match_id)
    return match_df

@st.cache_data()
def load_all_shots(columns):
    all_shots = pd.DataFrame()
    all_comps = load_competition_data()
    all_comps = all_comps[(all_comps['competition_gender']=='male')]
    for i, each_comp in all_comps.iterrows():
            fixtures = load_event_data(each_comp['competition_id'], each_comp['season_id'])
            for fixture in fixtures:
                a_match = load_match_data(fixture['match_id'])
                a_match = a_match[(a_match['type_name']=='Shot') & (a_match['shot_type_name']=='Open Play')]
                a_match = a_match[columns]
                a_match['goal'] = a_match['shot_outcome_name'].apply(goal_yes_no)
                a_match['distance_from_goal'] = a_match['location'].apply(get_distance_from_goal)
                a_match['angle'] = a_match['location'].apply(get_angle)
                a_match['opposition_blocking'] = a_match.apply(
                    lambda row: get_blocking_players(
                        row['shot_freeze_frame'], row['location']
                    ), axis=1
                )
                a_match['all_blocking'] = a_match.apply(
                    lambda row: get_blocking_players_include_team(
                        row['shot_freeze_frame'], row['location']
                    ), axis=1
                )
                all_shots = pd.concat([all_shots, a_match])
    return all_shots

## Functions for displaying data ###################################################################

@st.cache_data
def draw_shot_histogram(shots):
    fig, ax = createHalf(120, 80, 'yards', 'gray')
    fig.patch.set_alpha(0)

    for i, shot in shots.iterrows():
        prev_x = shot['location'][0]
        prev_y = shot['location'][1]

        x = prev_y
        y = 60 - (120 - prev_x)
        
        circle_size = 2

        shot_circle = plt.Circle((x, y), circle_size, color='darkorange')
        shot_circle.set_alpha(.01)
        ax.add_patch(shot_circle)

    # Draw the shotmaps
    st.subheader('Shot Map')
    st.pyplot(fig)

## Machine learning functions ######################################################################

def train_and_fit_logistic_regression(target, shots, features):
    df = shots.copy()
    df = df.loc[df['shot_body_part_name'] != 'Head', features].reset_index(drop=True).copy()
    X = df.drop([target], axis=1)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)
    sb_xg = X_test['shot_statsbomb_xg']
    X_train = X_train.drop(['shot_statsbomb_xg'], axis=1)
    X_test = X_test.drop(['shot_statsbomb_xg'], axis=1)
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    st.write('Confusion Matrix')
    st.write(str(round(accuracy_score(y_pred,y_test),4)))
    st.write(confusion_matrix(y_test, y_pred))
    return model, y_pred, X_test
    

## Main script #####################################################################################

st.title('Generating xG from goals scored')

shots = load_all_shots(['location', 'shot_statsbomb_xg', 'shot_outcome_name', 'shot_type_name', 'shot_freeze_frame', 'shot_body_part_name'])

# draw_shot_histogram(shots)

model, y_pred, shot_test = train_and_fit_logistic_regression('goal', shots, ['distance_from_goal', 'angle', 'opposition_blocking', 'goal', 'shot_statsbomb_xg'])

shots_goal = shots[shots['goal']==1]
shots_missed = shots[shots['goal']==0]
shots_missed.reset_index(drop=True, inplace=True)
shots_missed_reduced = shots_missed.loc[:2368]

shots_v2 = pd.concat([shots_goal, shots_missed_reduced])
model, y_pred , shot_test = train_and_fit_logistic_regression('goal', shots_v2, ['distance_from_goal', 'angle', 'opposition_blocking', 'goal', 'shot_statsbomb_xg'])

# def is_equal(a, b):
#     if (a==b):
#         return 1
#     else:
#         return 0
# shot_test['my_pred'] = y_pred
# shot_test['sb_pred'] = shot_test['xg'].apply(lambda x: 1 if x>=0.5 else 0)
# shot_test['my_correct'] = shot_test.apply(lambda row: is_equal(row['my_pred'], row['goal']), axis=1)
# shot_test['sb_correct'] = shot_test.apply(lambda row: is_equal(row['sb_pred'], row['goal']), axis=1)

