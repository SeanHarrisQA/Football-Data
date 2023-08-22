import pandas as pd
import json
import numpy as np
import math
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import streamlit as st

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
    try:
        ans = math.degrees(math.acos(cosRSL))
        ans2 = math.degrees(math.atan(cosRSL))
        print(ans, ans2)
        return ans
    except ValueError as e:
        print('Tried: ' + str(cosRSL))
        return cosRSL

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
    
## Functions for loading data ######################################################################

filepath = '../../Python Learning/open-data/data/'

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

## Functions to train and fit models ###############################################################

def train_and_fit_decision_tree(target, shots, features):
    df = shots.copy()
    df = df.loc[(df['shot_type_name'] == 'Open Play') & (df['shot_body_part_name'] != 'Head'), features].reset_index(drop=True).copy()
    X = df.drop([target], axis=1)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)
    dtree_regressor = DecisionTreeRegressor()
    dtree_regressor.fit(X_train, y_train)
    y_pred = dtree_regressor.predict(X_test)
    fig, ax = plt.subplots(figsize=(7,7))
    fig.patch.set_alpha(0)
    plt.plot([0,1], linestyle='dotted', color='white')
    y_test_array = y_test.to_numpy()
    plt.scatter(y_pred, y_test_array, s=1)
    ax.set_xlabel('Predicted Values')
    ax.set_label('Test Values')
    st.pyplot(fig, transparent=True)
    mae = round(mean_absolute_error(y_test, y_pred), 6)
    st.write('Mean Absolute Error: ' + str(mae))
    r2 = round(r2_score(y_test, y_pred), 6)
    st.write("R-squared: " + str(r2))
    
def train_and_fit_random_forest(target, shots, features):
    df = shots.copy()
    df = df.loc[(df['shot_type_name'] == 'Open Play') & (df['shot_body_part_name'] != 'Head'), features].reset_index(drop=True).copy()
    X = df.drop([target], axis=1)
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)
    rf_regressor = RandomForestRegressor(n_estimators=1500, random_state=0)
    rf_regressor.fit(X_train, y_train)
    y_pred = rf_regressor.predict(X_test)
    fig, ax = plt.subplots(figsize=(7,7))
    fig.patch.set_alpha(0)
    plt.plot([0,1], linestyle='dotted', color='white')
    plt.scatter(y_pred, y_test, s=1)
    ax.set_xlabel('Predicted Values')
    ax.set_label('Test Values')
    st.pyplot(fig, transparent=True)
    mae = round(mean_absolute_error(y_test, y_pred), 6)
    st.write('Mean Absolute Error: ' + str(mae))
    r2 = round(r2_score(y_test, y_pred), 6)
    st.write("R-squared: " + str(r2))

# @st.cache_data
def train_and_fit_gradient_boosting(target, shots, features, params):
    gbr = GradientBoostingRegressor(**params)
    df = shots.copy()
    df = df.loc[(df['shot_type_name'] == 'Open Play') & (df['shot_body_part_name'] != 'Head'), features].reset_index(drop=True).copy()
    X = df.drop(['shot_statsbomb_xg'], axis=1)
    y = df['shot_statsbomb_xg']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=41)
    gbr.fit(X_train, y_train)
    y_pred = gbr.predict(X_test)
    fig, ax = plt.subplots(figsize=(7,7))
    fig.patch.set_alpha(0)
    plt.plot([0,1], linestyle='dotted', color='white')
    plt.scatter(y_pred, y_test, s=1)
    ax.set_xlabel('Predicted Values')
    ax.set_label('Test Values')
    st.pyplot(fig, transparent=True)
    mae = round(mean_absolute_error(y_test, y_pred), 6)
    st.write('Mean Absolute Error: ' + str(mae))
    r2 = round(r2_score(y_test, y_pred), 6)
    st.write("R-squared: " + str(r2))
    
def feature_selection(target, shots, features):
    df = shots.copy()
    df = df.loc[df['shot_type_name'] == 'Open Play', features].reset_index(drop=True).copy()
    X = df.drop([target], axis=1)
    y = df[target]
    f_selector = SelectKBest(score_func=f_regression, k='all')
    f_selector.fit(X,y)
    X_fs = f_selector.transform(X)
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0)
    
    ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
    plt.xlabel("Features")
    plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
    plt.ylabel("F-value (transformed from the correlation values)")
    st.pyplot(fig, transparent=True)
    f_selector = SelectKBest(score_func=mutual_info_regression, k='all')
    f_selector.fit(X,y)
    X_fs = f_selector.transform(X)
    fig, ax =plt.subplots()
    fig.patch.set_alpha(0)
    ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
    plt.xlabel("Features")
    plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
    plt.ylabel("Estimated MI Values")
    st.pyplot(fig, transparent=True)

## Main script #####################################################################################
st.title('Estimating xG')
plt.style.use('dark_background')

shots = load_all_shots(['location', 'shot_statsbomb_xg', 'shot_outcome_name', 'shot_type_name', 'shot_freeze_frame', 'shot_body_part_name'])

st.subheader('Using a decision tree regressor')
features = ['distance_from_goal', 'angle', 'shot_statsbomb_xg', 'opposition_blocking']
train_and_fit_decision_tree('shot_statsbomb_xg', shots, features)


st.subheader('Feature selection techniques')
features = ['distance_from_goal', 'angle', 'shot_statsbomb_xg', 'opposition_blocking']
feature_selection('shot_statsbomb_xg', shots, features)

st.subheader('Using a random forest regressor')
train_and_fit_random_forest('shot_statsbomb_xg', shots, features)

st.subheader('Using a gradient boosting regressor')
gbr_params = {'n_estimators': 1500,
          'max_depth': 3,
          'min_samples_split': 5,
          'learning_rate': 0.01,
          'loss': 'absolute_error'}
train_and_fit_gradient_boosting('shot_statsbomb_xg', shots, features, gbr_params)

st.subheader('Using a gradient boosting regressor')
gbr_params = {'n_estimators': 1500,
          'max_depth': 3,
          'min_samples_split': 5,
          'learning_rate': 0.01,
          'loss': 'squared_error'}
train_and_fit_gradient_boosting('shot_statsbomb_xg', shots, features, gbr_params)