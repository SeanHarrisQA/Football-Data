import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from seaborn import load_dataset
from sklearn.compose import make_column_transformer
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn import metrics

st.title('Machine Learning - Estimating expected goals')

# Global variables
filepath = '../../Python Learning/open-data/data/'
player_id = 5503
# Session State also supports attribute based syntax
if 'count' not in st.session_state:
    st.session_state.count = 0

@st.cache_data(show_spinner=False)
def load_event(local, match_id):
    if local:
        with open(filepath + '/events/' + str(match_id) + '.json') as f:
            event = json.load(f)
            event = pd.json_normalize(event, sep='_').assign(match_id=match_id)
    else:
        # event = sb.events(match_id=match_id)
        pass
    return event

###############################################################################
# 1 - Load relevant data ######################################################

st.subheader('Loading Data')

with open(filepath + '/matches/11/' + '24' + '.json') as f:
    all_matches = json.load(f)
    all_matches = pd.json_normalize(all_matches, sep='_').reset_index(drop=True)
progress_text = "Loading season actions. Please wait."
my_bar = st.progress(0, text=progress_text)
iteration_prcnt = 100 // len(all_matches)
progress = 0
season_actions = pd.DataFrame()
for i, match in all_matches.iterrows():
    # Load match
    event = load_event(True, match['match_id'])
    # Take all the events that involved that player
    bool = (event['player_id'] == player_id) | (event['pass_recipient_id'] == player_id)
    actions = event[bool]
    season_actions = pd.concat([season_actions, actions])
    progress+=iteration_prcnt
    my_bar.progress(progress, text=progress_text)
my_bar.progress(100, text='Data successfully loaded')
my_bar.empty()
season_actions.reset_index(drop=True, inplace=True)

st.dataframe(season_actions)

# Convert to just shots for messi
bool = (season_actions['type_name'] == 'Shot') & (season_actions['player_id'] == player_id)
all_shots = season_actions[bool].reset_index(drop=True).copy()



###############################################################################
# 1A - Preparing Data #########################################################

# Prepare a dataframe with relevant features for each shot such as distacnce
# from goal, parts of object freeze frame maybe angle to goal, shot body part
# shot type etc

# keep useful columns from all_shots
all_shots = all_shots[['play_pattern_name', 'shot_freeze_frame', 'location', 'shot_type_name', 'shot_technique_name', 'shot_body_part_name','shot_statsbomb_xg', 'shot_first_time']]
# modify data in all shots
# isolate x coordinate so we can process it
def get_x(point):
    return point[0]
all_shots['x_location'] = all_shots['location'].apply(get_x)
# isolate y coordinate so we can process it
def get_y(point):
    return point[1]
all_shots['y_location'] = all_shots['location'].apply(get_y)

# find out how many opposition players are involved in the play
def get_opposition_involved(arr):
    if type(arr) is list:
        opp_count = 0
        for i in range(len(arr)):
            if arr[i]['teammate'] == False:
                opp_count+=1
        return opp_count
    else:
        return 0
all_shots['opposition_involved'] = all_shots['shot_freeze_frame'].apply(get_opposition_involved)

# drop further columns that aren't needed now we have calculated further data 
# such as loaction once we have x and y
all_shots.drop(['location', 'shot_freeze_frame'], axis=1, inplace=True)
st.dataframe(all_shots.head())

# One hot encoding my categorical data
st.write('My data')
categorical_columns = ['play_pattern_name', 'shot_type_name', 'shot_technique_name', 'shot_body_part_name', 'shot_first_time']
transformer = make_column_transformer(
    (OneHotEncoder(), categorical_columns),
    remainder='passthrough')
transformed = transformer.fit_transform(all_shots)
transformed_df = pd.DataFrame(transformed, columns=transformer.get_feature_names_out())
st.write(transformed_df.head())

# clean columns
current_names = transformed_df.columns
new_names = []
for i in range(len(current_names)):
    new_name = current_names[i].lower().replace('onehotencoder__', '').replace('remainder__', '').replace('_', ' ')
    new_names.append(new_name)
transformed_df.columns = new_names
st.write(transformed_df.head())

###############################################################################
# 2 - Feature selection #######################################################

st.write('Correlation')
X = transformed_df.drop(['shot statsbomb xg'], axis=1)
y = transformed_df['shot statsbomb xg']

f_selector = SelectKBest(score_func=f_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("F-value (transformed from the correlation values)")
st.pyplot(fig)

f_selector = SelectKBest(score_func=mutual_info_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("Estimated MI Values")
st.pyplot(fig)

# Take a look at different values
X['y location'] = abs(40 - X['y location'])
transformed_df['y location'] = abs(40 - transformed_df['y location'])
st.write(X.head())
st.write(X.describe())

st.subheader('Repeat Experiment')
st.write('Correlation')

f_selector = SelectKBest(score_func=f_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("F-value (transformed from the correlation values)")
st.pyplot(fig)

f_selector = SelectKBest(score_func=mutual_info_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("Estimated MI Values")
st.pyplot(fig)

non_categorical_df = transformed_df[['x location', 'y location', 'opposition involved', 'shot statsbomb xg']]
st.pyplot(sns.pairplot(non_categorical_df))

###############################################################################
# 3 - Training ################################################################

X = non_categorical_df.drop(['shot statsbomb xg'], axis=1)
y = non_categorical_df['shot statsbomb xg']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=41)

model = LinearRegression()

model.fit(X_train, y_train)

st.write(pd.DataFrame(model.coef_, X.columns, columns = ['Coeff']))

predictions = model.predict(X_test)

fig, ax = plt.subplots()
plt.plot([0,1], linestyle='dotted', color='black')
plt.scatter(y_test, predictions)
st.pyplot(fig)

###############################################################################
# 4 - Evaluation ##############################################################

st.write('MAE')
st.write(metrics.mean_absolute_error(y_test, predictions))
st.write('MSE not appropriate for this scenario')
st.write(metrics.mean_squared_error(y_test, predictions))

###############################################################################
# 5 - 2nd Attempt #############################################################

# i add penalty column as well as angle and distance 

st.subheader("Refining the model")
all_shots
focused_df = all_shots.drop(['play_pattern_name', 'shot_technique_name', 'shot_body_part_name'], axis=1)
categorical_columns = ['shot_type_name']
transformer = make_column_transformer(
    (OneHotEncoder(), categorical_columns),
    remainder='passthrough')
transformed = transformer.fit_transform(all_shots)
transformed_df = pd.DataFrame(transformed, columns=transformer.get_feature_names_out())
st.write(transformed_df.head())

# clean columns
current_names = transformed_df.columns
new_names = []
for i in range(len(current_names)):
    new_name = current_names[i].lower().replace('onehotencoder__', '').replace('remainder__', '').replace('_', ' ')
    new_names.append(new_name)
transformed_df.columns = new_names
st.write(transformed_df.head())

###############################################################################
# 5 2 Feature selection #######################################################

st.write('Correlation')
X = transformed_df.drop(['shot statsbomb xg'], axis=1)
y = transformed_df['shot statsbomb xg']

f_selector = SelectKBest(score_func=f_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("F-value (transformed from the correlation values)")
st.pyplot(fig)

f_selector = SelectKBest(score_func=mutual_info_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("Estimated MI Values")
st.pyplot(fig)

# Take a look at different values
X['y location'] = abs(40 - X['y location'])
transformed_df['y location'] = abs(40 - transformed_df['y location'])
st.write(X.head())
st.write(X.describe())

st.subheader('Repeat Experiment')
st.write('Correlation')

f_selector = SelectKBest(score_func=f_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("F-value (transformed from the correlation values)")
st.pyplot(fig)

f_selector = SelectKBest(score_func=mutual_info_regression, k='all')
f_selector.fit(X,y)
X_fs = f_selector.transform(X)

fig, ax =plt.subplots()
ax.bar([i for i in range(len(f_selector.scores_))], f_selector.scores_)
plt.xlabel("Features")
plt.xticks(ticks=range(len(X.columns)), labels=X.columns, rotation=90)
plt.ylabel("Estimated MI Values")
st.pyplot(fig)

non_categorical_df = transformed_df[['x location', 'y location', 'opposition involved', 'shot statsbomb xg']]
st.pyplot(sns.pairplot(non_categorical_df))

###############################################################################
# 5 3 Training ################################################################

X = non_categorical_df.drop(['shot statsbomb xg'], axis=1)
y = non_categorical_df['shot statsbomb xg']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=41)

model = LinearRegression()

model.fit(X_train, y_train)

st.write(pd.DataFrame(model.coef_, X.columns, columns = ['Coeff']))

predictions = model.predict(X_test)

fig, ax = plt.subplots()
plt.plot([0,1], linestyle='dotted', color='black')
plt.scatter(y_test, predictions)
st.pyplot(fig)

###############################################################################
# 5 4 Evaluation ##############################################################

st.write('MAE')
st.write(metrics.mean_absolute_error(y_test, predictions))
st.write('MSE not appropriate for this scenario')
st.write(metrics.mean_squared_error(y_test, predictions))




