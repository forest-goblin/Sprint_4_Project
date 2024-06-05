import streamlit as st



import plotly.express as px
import streamlit as st
import pandas as pd
import scipy.stats


import dash
from dash import Dash
import dash_core_components as dcc
from dash import html
from dash.dependencies import Input, Output, State

steam = pd.read_csv('C:/Users/Donah/Documents/git/projects/Sprint_4_Project/steam_games.csv')

app =Dash(__name__)

app.layout = html.Div([
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

if __name__ == '__main__':
    app.run_server(debug=True)
    