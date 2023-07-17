import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from FCPython import createPitch
import streamlit as st
import math
import matplotlib as mpl

# @st.cache_data(max_entries=20)
def draw_passmap(game, player, values):
    # Pass map for given player
    st.subheader('Pass Map')
    mn, mx = values
    # Select rows all the rows where the given player makes a pass
    bool = (game['player_name'] == player) & (game['type_name'] == 'Pass') & (game['minute'] >= mn) & (game['minute'] <= mx)
    # Counter to monitor pass success rate
    successful_passes = 0

    passes = game.loc[bool, ['pass_length', 'pass_angle', 'pass_end_location', 'location', 'player_name', 'pass_body_part_name', 'pass_outcome_id']]
    # Create plot
    fig, ax = createPitch(pitch_length, pitch_width, 'yards', 'white')
    fig.patch.set_alpha(0)
    # Plot the passes
    for a_pass in passes.iterrows():
        #length = a_pass[1][0]
        #angle = a_pass[1][1]
        complete = math.isnan(a_pass[1][6]) or a_pass[1][6] == 76
        x_end = a_pass[1][2][0] 
        y_end = pitch_width-a_pass[1][2][1]
        x_start = a_pass[1][3][0]
        y_start = pitch_width-a_pass[1][3][1]
        if complete:
            successful_passes+=1
            plt.arrow(x_start, y_start, x_end-x_start, y_end - y_start, color='mediumorchid', head_width=1.5, head_length=2, length_includes_head=True)
        else:
            plt.arrow(x_start, y_start, x_end-x_start, y_end - y_start, color='darkorange', head_width=1.5, head_length=2, length_includes_head=True)
    # Show the plot on the page
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    pass_success_rate = round((successful_passes / len(passes)) * 100)
    st.write(str(pass_success_rate) + '% Successful')
    plt.text(2, 76, 'Successful', color='mediumorchid')
    plt.text(100, 76, 'Unsuccessful', color='darkorange')
    st.pyplot(fig)
    st.caption('Direction of play from left to right')
    st.divider()

# @st.cache_data(max_entries=20)
def draw_heatmap(game, player):
    # Heatmap for a given player
    st.subheader('Heat Map')
    # Initalise heats - N.B the way the pitch heights are initialised means there is no need to flip the coordinates
    # in the y-axis as with other functions
    heats = np.zeros((121,81), int)
    # Drop unnecessary rows
    bool = (game['player_name'] == player) & (game['location'].notnull()) #& (game['period'] == 1)
    player_touches = game[bool]
    # Iterate through the rows and calculate the location of every touch
    for i, touch in player_touches.iterrows():
        x = np.round(touch['location'][0]).astype(int)
        y = np.round(touch['location'][1]).astype(int)
        # heats[x-3:x+4, y-3:y+4] += 3
        # heats[x-1:x+2, y-1:y+2] += 6
        heats[x-3:x+4, y-1:y+2] += 3
        heats[x-1:x+2, y-3:y+4] += 3
        heats[x-2:x+3, y-2:y+3] += 3
        heats[x-2:x+3, y] += 1
        heats[y, x-2:x+3] += 1
        heats[x-1:x+2, y-1:y+2] +=1
        heats[x,y] +=1
    # Plot heatmap
    fig, ax = createPitch(pitch_length, pitch_width, 'yards', 'white')
    plt.imshow(np.transpose(heats), cmap='magma')
    fig.patch.set_alpha(0)
    st.pyplot(fig)
    st.caption('Direction of play from left to right')
    st.divider()

def draw_simple_sonar(game, player):
    fig, ax = createPitch(pitch_length, pitch_width, 'yards', 'gray')
    fig.patch.set_alpha(0)
    bool = (game['player_name'] == player) & (game['type_name'] == 'Pass')
    passes = game.loc[bool, ['pass_length', 'pass_angle', 'pass_end_location', 'location', 'player_name', 'pass_body_part_name', 'pass_outcome_id']]
    passes.reset_index(drop=True, inplace=True)
    # passes = passes.loc[:10]
    for i, a_pass in passes.iterrows():
        angle = a_pass['pass_angle']
        x_end = a_pass['pass_end_location'][0] + (60 - a_pass['location'][0])
        y_end = pitch_width - (a_pass['pass_end_location'][1] + (40 - a_pass['location'][1]))
        x_start = a_pass['location'][0] + (60 - a_pass['location'][0])
        y_start = pitch_width - (a_pass['location'][1] + (40 - a_pass['location'][1]))
        if angle > 0:
            plt.arrow(x_start, y_start, x_end-x_start, y_end - y_start, color='yellow', head_width=1.5, head_length=2, length_includes_head=True)
        else:
            plt.arrow(x_start, y_start, x_end-x_start, y_end - y_start, color='blue', head_width=1.5, head_length=2, length_includes_head=True)    
    st.pyplot(fig)

def draw_passing_sonar(game, player):
    bool = (game['player_name'] == player) & (game['type_name'] == 'Pass')
    passes = game.loc[bool, ['pass_length', 'pass_angle', 'pass_end_location', 'location', 'player_name', 'pass_body_part_name', 'pass_outcome_id']]
    passes.reset_index(drop=True, inplace=True)
    directions = np.zeros(shape=(3, 16), dtype=float)
    divisor = (2*np.pi) / 16
    for i, a_pass in passes.iterrows():
        angle = a_pass['pass_angle']
        completed = math.isnan(a_pass['pass_outcome_id'])# or a_pass['pass_outcome_id'] == 76
        distance = a_pass['pass_length']
        if abs(angle) < np.pi:
            direction_index = np.round((angle // divisor) + 8).astype(int)
            directions[0, direction_index] += 1
            directions[2, direction_index] = (distance + (directions[2, direction_index] * (directions[0, direction_index]-1))) / directions[0, direction_index]
            if completed:
                directions[1, direction_index] += 1

    for i in range(len(directions)):
        directions[i] = directions[i][::-1]

    # Normalise the values in the directions chart so that they cqn be plotted simply
    max_no_of_passes = max(directions[0])
    def normalise_helper(num):
        return num / max_no_of_passes
    normalise = np.vectorize(normalise_helper)
    directions_normalised = normalise(directions[:2])

    # Now draw the piechart, three seperate piecharts need to be created, one invisible chart so that wedges can have dirrent radii
    data = [1 for x in range(16)]
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_alpha(0)

    # hold = [0 for x in range(16)]
    # cbar = plt.colorbar(ax.scatter(x=hold, y=hold, c=directions[2], cmap='magma'), shrink=0.5, anchor=(-0.5, 0.5))
    # cbar_ticks =plt.getp(cbar.ax.axes, 'yticklabels')
    # plt.getp(cbar.ax.axes)
    # plt.setp(cbar_ticks, color='white')
    # cbar_lines =plt.getp(cbar.ax.axes, 'yticklines')
    # plt.setp(cbar_lines, color='white')
    # Define colourmap for plotting the passing distances
    magma_colourmap = mpl.colormaps['magma'].resampled(8)
    d_cmap_v = calculate_cmap_values(directions[2])

    # st.write('Max avg _distance:', max_avg_distance)
    sa = (360 * 5) / len(data)
    for i in range(16):
        outer_wedges, texts = ax.pie(data, radius=max(0.05, directions_normalised[0, i]), startangle=-90)
        inner_wedges, texts_1 = ax.pie(data, radius=max(0.05, directions_normalised[0, i]), startangle=-90)
        c = magma_colourmap(d_cmap_v[i])
        for j in range(16):
            outer_wedges[j].set_visible(False)
            inner_wedges[j].set_visible(False)
        outer_wedges[i].set_visible(True)
        outer_wedges[i].set_color('gray')
        outer_wedges[i].set_edgecolor('white')
        inner_wedges[i].set_visible(True)
        inner_wedges[i].set_color(c)
        inner_wedges[i].set_edgecolor('white')
    # ax.scatter(x=data, y=data, c=directions[2], cmap='magma')
    # ax.set_title("Matplotlib bakery: A pie", c='w', loc='left', pad=-30)
    # plt.savefig('image.png', bbox_inches='tight', pad_inches=0)
    
    st.pyplot(fig)

def calculate_cmap_values(arr):
    mn = min(arr) - 2
    mx = max(arr)
    diff = mx-mn
    values = [(x - mn) / diff for x in arr]
    return values

# Variables used throughout the script
pitch_length = 120
pitch_width = 80

# Main method
if 'df' in st.session_state:
    game = st.session_state.df
    players = game['player_name'].dropna().unique()
else:
    st.warning('Please return to the home page and select a match')

selected_player = st.sidebar.radio("Select a team", (players))

st.title('Player analysis')
# Start of page
st.subheader(selected_player)
st.write(st.session_state.scoreline)
st.divider()

values = st.slider(
    'Select a range of values',
    0, 100, (0, 100))
st.write('Values:', values)

draw_passing_sonar(game, selected_player)
draw_simple_sonar(game, selected_player)
draw_passmap(game, selected_player, values)
draw_heatmap(game, selected_player)