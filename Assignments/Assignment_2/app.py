# Import all required libraries 

import pandas as pd
import numpy as np

from dash import dcc, html, Dash
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
import plotly.express as px


# Set up Dash object 
app = Dash(__name__)

app.layout = html.Div([
    html.H1('Election Results'),
    dcc.Dropdown(
        id='party-dropdown',
        options=[
            {'label': 'Democratic', 'value': 'democratic'},
            {'label': 'Republican', 'value': 'republican'}
        ],
        value='democratic'  # Set the initial value
    ),
    html.Div(id='output-container')
])


# Import relevant data for map (geojson + FIPS data)
df = pd.read_csv('prim_state_results.csv')

# Create the choropleth map
fig = px.choropleth(df,
                    locations='State',
                    color='Delegates',
                    hover_name='State',
                    hover_data=['Candidate', 'Party', 'Incumbent', 'Vote', 'Pct', 'Winner'],
                    color_continuous_scale='Blues',
                    scope='usa')

# Update the layout
fig.update_layout(
    geo=dict(
        scope='usa',
        showlakes=True,
        lakecolor='rgb(255, 255, 255)'
    )
)


# Show the HTML layout
app.layout = html.Div([
    html.H1('US Presidential Primary Election 2024'),
    dcc.Graph(figure=fig)
])



# Run the Dash app 
if __name__=='__main__':
    app.run_server(debug=True)