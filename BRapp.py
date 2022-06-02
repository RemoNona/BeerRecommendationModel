# APPLICATION FOR BEER RECOMMENDATIONS. COMMAND LINE PROMPT: streamlit run BRapp.py

import streamlit as st
import pandas as pd
import numpy as np
import sys
sys.tracebacklimit = 0


# Reaad and set up files
users = pd.read_pickle('./files/users.pickle')
main = pd.read_pickle('./files/main.pickle')
beers = pd.read_pickle('./files/beers.pickle')
beers = beers[['beer_name', 'brewery_name']]

#=========================================================================================================================================================
############ BEER ALGORITHM ############

def recBeer(selection, rating, topX):
    '''
    Function to find beer recommendations based on beer preferences.
    Accepts list or set or beer names, as well as custom rating threshold and 
    number of recommendations threshold.
    Function prints out list of users in cluster and number of users in
    cluster.
    Returns dataframe of beer recommendations.
    '''
    styles = []
    for beer in selection:
        styles.append(main[ main.beer_name==beer].iloc[0]['beer_style'])
    styles = set(styles)
    cluster_users = []

    # Check to see what users reviewed these beers the highest
    for user in users.user_beers.items():
        count = 0
        for beer in selection:
            if beer in user[1]:
                count += 1
        if count == len(selection):
            cluster_users.append(user[0])

    # These are the beers new user should try in the preferred styles. 
    beer_to_suggest = pd.DataFrame()

    for user in cluster_users:
        temp = users.loc[user, 'user_beers']
        df = pd.DataFrame(temp, index=['beer_beerid', 'brewery_name', 'beer_style', 'review_overall']).transpose()
        
        for style in styles:
            beer_to_suggest = pd.concat([beer_to_suggest, df[ (df.beer_style==style) & (df.review_overall >= rating) ]])

    beer_to_suggest['beer_name'] = beer_to_suggest.index.copy()
    try:
        beer_to_suggest.groupby(['beer_beerid', 'beer_name', 'brewery_name', 'beer_style'])
    except KeyError:
        raise Exception("You are unique! No one else loves these beers as much as you do.")
        
    beer_to_suggest = pd.DataFrame(beer_to_suggest.groupby(['beer_beerid', 'beer_name', 'brewery_name', 'beer_style'])['review_overall'].mean().round(2))
    beer_to_suggest = beer_to_suggest.reset_index([1,2,3]).sort_values(['review_overall'], ascending=False)

    rec = pd.DataFrame()
    for style in styles:
        rec = pd.concat([rec, beer_to_suggest[ beer_to_suggest.beer_style==style ][:topX]])

    return rec

############ END BEER ALGORITHM ############
#=========================================================================================================================================================
############ STYLE ALGORITHM ############
def recStyle(styles, rating, topX):
    '''
    Function to provide beer recommendations based on style preferences.
    Accepts a list/set of styles, custom rating threshold, and 
    number of recommendations threshold.
    Function prints out list of users in cluster and number of users in
    cluster.
    Returns dataframe of beer recommendations.
    '''
    # Check to see what users review these styles the most
    # and give rating of 4.25 (or user specified) or higher.
    styles = set(styles)
    users_reviewed = []
    for i in range(len(users)):
        temp = users.iloc[i, : ]
        name = temp.name
        for style in styles:
            if style in temp[1]:
                if temp[1][style] >= rating:
                    users_reviewed.append((name, style, temp[1][style]))

    count = pd.DataFrame(users_reviewed, columns=['user', 'style', 'rating']).groupby('user').count()['style']

    cluster_users = []
    for i in count.items():
        if i[1] == len(styles):
            cluster_users.append(i[0])

    # These are the beers new user should try in the preferred styles. 
    beer_to_suggest = pd.DataFrame()

    for user in cluster_users:
        temp = users.loc[user, 'user_beers']
        df = pd.DataFrame(temp, index=['beer_beerid', 'brewery_name', 'beer_style', 'review_overall']).transpose()
        
        for style in styles:
            beer_to_suggest = pd.concat([beer_to_suggest, df[ (df.beer_style==style) & (df.review_overall >= rating) ]])

    beer_to_suggest['beer_name'] = beer_to_suggest.index.copy()

    try:
        pd.DataFrame(beer_to_suggest.groupby(['beer_beerid', 'beer_name', 'brewery_name', 'beer_style']))
    except KeyError:
        raise Exception("You are unique! No one else loves these styles as much as you do.")

    beer_to_suggest = pd.DataFrame(beer_to_suggest.groupby(['beer_beerid', 'beer_name', 'brewery_name', 'beer_style'])['review_overall'].mean().round(2))
    beer_to_suggest = beer_to_suggest.reset_index([1,2,3]).sort_values(['review_overall'], ascending=False)

    rec = pd.DataFrame()
    for style in styles:

        rec = pd.concat([rec, beer_to_suggest[ beer_to_suggest.beer_style==style ][:topX]])

    return rec

############ END STYLE ALGORITHM ############
#=========================================================================================================================================================
#=========================================================================================================================================================
############ STREAMLIT DASHBOARD ############
# Set dashboard layout 
st.set_page_config(layout="wide")
c1, c2 = st.columns((1, .5))
algo = c2.radio('What would you like a recommendation for?', ['Beer', 'Beer-style'])

# BEER RECOMMENDATION
if algo == 'Beer':

    breweries = list(beers.brewery_name.unique())
    breweries.sort()
    num_beers = c2.selectbox("Number of favorites beers you'd like to enter:", [b for b in range(1, 11)])
    num_recs = c2.selectbox("Number of beer recommendations you'd like to recieve:", [1, 5, 10, 20])
    rating = c2.selectbox('Rating Threshold:', [4.0, 4.25, 4.5, 4.75, 5.0])
    selection = []

    for i in range(1,num_beers+1):
        brewery = c2.selectbox(f'{i} - Brewery: ', breweries)
        beers_ = list(beers.beer_name[beers.brewery_name == brewery].unique())
        beers_.sort()
        beer_choice =  c2.selectbox(f'{i} - Beer', beers_)
        selection.append(beer_choice)

    selection = set(selection)
    try:
        recBeer(selection, topX=num_recs, rating=rating).set_index('review_overall')
    except KeyError:
        raise Exception("You are unique! No one else loves these beers as much as you do.")
    c1.dataframe(recBeer(selection, topX=num_recs, rating=rating).set_index('review_overall'), height=900)
    # Row was a quick set up for test case parameters than can be copied into spreadsheet
    row = f"test case: {np.nan},{algo},{np.nan},{num_beers},{num_recs},{rating},{np.nan},{selection}"
    c2.text(row)
#=========================================================================================================================================================

# STYLE RECOMMENDATION
else:
    styles = list(main.beer_style.unique())
    styles.sort()
    num_styles = c2.selectbox("Number of beer-styles you'd like to enter:", [1, 2, 3, 4, 5])
    num_recs = c2.selectbox("Number of beer recommendations you'd like to recieve:", [1, 5, 10, 20])
    rating = c2.selectbox('Rating Threshold:', [4.0, 4.25, 4.5, 4.75, 5.0])
    selection = []

    for i in range(1,num_styles+1):
        beer_style = c2.selectbox(f'{i} - Style: ', styles)
        selection.append(beer_style)

    selection = set(selection)
    try:
        recStyle(selection, topX=num_recs, rating=rating)
    except KeyError:
        raise Exception("You are unique! No one else loves these styles as much as you do.")
    c1.dataframe(recStyle(selection, topX=num_recs, rating=rating).set_index('review_overall'), height=900)
    # Row was a quick set up for test case parameters than can be copied into spreadsheet
    row = f"test case: {np.nan},{algo},{num_styles},{np.nan},{num_recs},{rating},{selection},{np.nan}"
    c2.text(row)

############ END STREAMLIT DASHBOARD ############
