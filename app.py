import streamlit as st

import plotly.express as px
import streamlit as st
import pandas as pd
import scipy.stats

import dash
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State


steam = pd.read_csv('steam_games.csv')

st.header('Steam Store Data')
st.divider() 
#Header info



best_rec = steam[['overall_review_count', 'title']]
best_rec = best_rec.dropna()
best_rec= best_rec.sort_values(by='overall_review_count',ascending=False).head(20)
#games with the most reviews

top_awards = steam[['awards','genres']]
top_awards = top_awards.dropna()
top_awards = top_awards.sort_values('awards',ascending=False).head(20)
#top awards

highest_rev = steam[['overall_review_%', 'title']]
highest_rev = highest_rev.dropna()
highest_rev = highest_rev.sort_values(by='overall_review_%',ascending=False).head(20)
#games with the highest review scores


c1 = pd.DataFrame(best_rec, columns=["number_of_reviews", 'title'])
c2 =pd.DataFrame(highest_rev, columns=['percent', 'title2'])
c1 = best_rec.loc[~best_rec.index.duplicated(keep='first')]
c2 = highest_rev.loc[~highest_rev.index.duplicated(keep='first')]

combine_rec_rev = pd.concat([c1, c2], axis=0)
#merging data for graph 

count_g = pd.Series(steam['genres']).value_counts() 
most_gen = count_g.head(20)
bar_comp =[most_gen,[steam[['overall_review_count', 'overall_review_%']]]]
#Seperating data for graph

count_d =  steam[['developer', 'title']]
most_games = count_d.dropna()
dev_comp = most_games.sort_values(by='developer',ascending=False).head(20)

b1 = pd.DataFrame(dev_comp, columns=['developer', 'title'])
b1 = dev_comp.loc[~dev_comp.index.duplicated(keep='first')] 
d1=pd.DataFrame(highest_rev, columns=['percent', 'title2'])
d1=highest_rev.loc[~highest_rev.index.duplicated(keep='first')]

combine_dev = pd.concat([b1,d1], axis=0)
#merging data for graph


st.write("Through these graphs you will be able to explore the performance of game titles and developers on the gaming platform Steam.")
st.divider() 
#Graphing 
fig = px.bar(combine_rec_rev, x="title", y="overall_review_count",title="Top 20 Games with their Review Count and Review Percentage ", barmode="group",labels={
                     "title": "Game Titles",
                     "overall_review_count":"Review Count",
                 },
             )
st.write(fig)
st.divider() 

fig = px.scatter(top_awards, x="genres", y="awards",title="Top 20 genres with the most awards")
st.write(fig)


switch = st.checkbox("Look at Developer data")
switch2 = st.checkbox("Look at Game Title data")

#fig1 = px.bar(combine_dev, x="developer", y="title", color="overall_review_%", barmode="group")
app =Dash(__name__)

fig1 = app.layout = html.Div([
    html.Div([
        html.Label(['Game Genres']),
        dcc.Dropdown(
            id='my_drop',
            options=[
                {'label':'Recent Reviews', 'value' : 'recent_review'},
                {'label':'Overall Reviews', 'value' : 'overall_review'},
                {'label':'Awards', 'value' : 'awards'},
                {'label':'Overall Review Percent', 'value' : 'overall_review_%'},
            ],
            value='overall_review',
            multi=False,
            clearable=False,
            style={'width':'50%'}
        ),
     ]),


    html.Div([
         dcc.Graph(id='the_graph')
    ]),

])


@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_drop', component_property='value')]
)

def update_graph(my_drop):
    steam_info = steam

    piechart=px.pie(
        data_frame=steam_info,
        names=my_drop,
        hole=.3,
        )
    
    return(piechart)



fig2 = px.bar(combine_rec_rev, x="title", y="overall_review_count", color="overall_review_%", barmode="group")


if switch:
    st.write(fig1)

if switch2:
    st.write(fig2)

#Creating Check Boxes