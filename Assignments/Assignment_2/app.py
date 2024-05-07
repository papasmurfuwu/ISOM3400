from dash import Dash, dcc, html, Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
import json


# state code mapping
us_state_to_code = {
            "Alabama": "AL",
            "Alaska": "AK",
            "American samoa": "AS",
            "Arizona": "AZ",
            "Arkansas": "AR",
            "California": "CA",
            "Colorado": "CO",
            "Connecticut": "CT",
            "Delaware": "DE",
            "Florida": "FL",
            "Georgia": "GA",
            "Hawaii": "HI",
            "Idaho": "ID",
            "Illinois": "IL",
            "Indiana": "IN",
            "Iowa": "IA",
            "Kansas": "KS",
            "Kentucky": "KY",
            "Louisiana": "LA",
            "Maine": "ME",
            "Maryland": "MD",
            "Massachusetts": "MA",
            "Michigan": "MI",
            "Minnesota": "MN",
            "Mississippi": "MS",
            "Missouri": "MO",
            "Montana": "MT",
            "Nebraska": "NE",
            "Nevada": "NV",
            "New Hampshire": "NH",
            "New Jersey": "NJ",
            "New Mexico": "NM",
            "New York": "NY",
            "North Carolina": "NC",
            "North Dakota": "ND",
            "Ohio": "OH",
            "Oklahoma": "OK",
            "Oregon": "OR",
            "Pennsylvania": "PA",
            "Rhode Island": "RI",
            "South Carolina": "SC",
            "South Dakota": "SD",
            "Tennessee": "TN",
            "Texas": "TX",
            "Utah": "UT",
            "Vermont": "VT",
            "Virginia": "VA",
            "Washington": "WA",
            "West Virginia": "WV",
            "Wisconsin": "WI",
            "Wyoming": "WY",
            "District of Columbia": "DC",
            "American Samoa": "AS",
            "Guam": "GU",
            "Northern Mariana Islands": "MP",
            "Puerto Rico": "PR",
            "United States Minor Outlying Islands": "UM",
            "U.S. Virgin Islands": "VI",
        }

df = pd.read_csv('prim_state_results.csv', dtype={'Delegates': int})
df['State Code'] = df['State'].map(us_state_to_code)
df_winner = df.query("Winner == 'Yes'")
dem_winner_df = df_winner.query("Party == 'Democratic'")
rep_winner_df = df_winner.query("Party == 'Republican'")

app = Dash(__name__)

app.layout = html.Div([
                html.Br(),
                html.Div([
                        html.H1(children='US Presidential Primary Election 2024')
                        ]),
                html.Br(),
                html.Hr(),
                html.Div([    
                        html.Div([
                                dcc.Dropdown(id='party-dropdown',
                                             options=[
                                                {'label': 'Democratic', 'value': 'democratic'},
                                                {'label': 'Republican', 'value': 'republican'}
                                                ],
                                                value='democratic'),
                                dcc.Graph(id='choropleth-map', clear_on_unhover=True)],
                                style={'width': '60%', 'height':'600px', 'float':'left', 'display': 'inline'}
                                ),
                        html.Div([
                                html.Div([
                                        html.Br(),
                                        html.H2(children='', style={'textAlign':'center'}),
                                                dcc.Graph(id='state-graph')],
                                        style={'height':'50%', 'float':'centre', 'display': 'inline-block'},
                                ),
                         html.Div([
                                        html.H2(children='', style={'textAlign':'center'}),
                                                dcc.Graph()],
                                        style={'height':'50%', 'float':'centre', 'display': 'inline-block'}
                                )], 
                        
                         style={'width': '40%', 'height':'1200px', 'float':'centre', 'display': 'inline'}
                        ),
                 html.Hr(),
                 html.Br()
                 ])
            ])

@app.callback(
        Output('choropleth-map', 'figure'),
        Input('party-dropdown', 'value')
)
def plot_choropleth(selected_party):
    if selected_party == 'democratic':
        party_df = dem_winner_df
        colorscale = 'Blues'
    else:
        party_df = rep_winner_df
        colorscale = 'Redor'
        
    fig = go.Figure(data=go.Choropleth(
        locations = party_df['State Code'],
        z = party_df['Delegates'].astype(int),
        locationmode = 'USA-states',
        colorscale = colorscale,
        hovertemplate = '<b>%{customdata[5]}</b><br><br>' +
                  'Party: %{customdata[0]}<br>' +
                  'Winning Candidate: %{customdata[1]}<br>' +
                  'Votes: %{customdata[2]}<br>' +
                  'Incumbent: %{customdata[3]}<br>' +
                  'Delegates: %{customdata[4]}',
        customdata = party_df[['Party', 'Candidate', 'Vote', 'Incumbent', 'Delegates', 'State']],
        name = '' # Gets rid of 'trace 0' next to hoverdata
    ))

    fig.update_layout(
        geo=dict(scope='usa')
    )
 
    return fig 
   


@app.callback(
    Output('state-graph', 'figure'),
    Input('choropleth-map', 'hoverData'),
    Input('party-dropdown', 'value')
)
def update_barchart(hoverData, selected_party):
    # Filter the data for the selected state and party
    if selected_party == 'democratic':
        state_data = df[df['Party'] == 'Democratic']
        all_state = dem_winner_df
        candidate_colors = ['#1f77b4', 'darkgoldenrod']
    else:
        state_data = df[df['Party'] == 'Republican']
        all_state = rep_winner_df
        candidate_colors = ['#d62728', 'teal']

    if hoverData is None:
    # Return bar chart of y the number of delegates gained by winning candidates in all states
        fig_all = go.Figure()
        
        unique_candidates = all_state['Candidate'].unique()
        color_mapping = {candidate: color for candidate, color in zip(unique_candidates, candidate_colors)}

        for candidate in unique_candidates:
            candidate_data = all_state[all_state['Candidate'] == candidate]
            fig_all.add_trace(go.Bar(
                x = candidate_data['State'],  
                y = candidate_data['Delegates'],  
                hovertemplate = '<b>State: %{x}</b><br></br>' +
                            'Party: %{customdata[0]}<br>' +
                            'Winning Candidate: %{customdata[1]}<br>' +
                            'Delegates: %{customdata[2]}<extra></extra>',
                customdata = candidate_data[['Party', 'Candidate', 'Delegates']],  
                marker_color = color_mapping[candidate],  
                textposition = 'auto'
            ))

        fig_all.update_layout(
            title='Delegates earned from each state',
            title_x=0.5,
            xaxis_title='State',
            yaxis_title='Delegates',
            yaxis=dict(dtick=50),
            xaxis=dict(dtick=1),
            showlegend=True
        )

        return fig_all
    
    state = hoverData['points'][0]['customdata'][-1]
    state_data = state_data[state_data['State'] == state]

    fig = go.Figure()
    for i, candidate in enumerate(state_data['Candidate'].unique()):
        candidate_data = state_data[state_data['Candidate'] == candidate]
        
        fig.add_trace(go.Bar(
            x = candidate_data['Candidate'],
            y = candidate_data['Delegates'],
            hovertemplate = '<b>State: %{customdata[0]}</b><br></br>' +
                          'Party: %{customdata[1]}<br>' +
                          'Candidate: %{x}<br>' +
                          'Votes: %{customdata[2]}<extra></extra>',
            customdata = candidate_data[['State', 'Party', 'Vote']],
            marker_color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)], # Cycle through colours in colour palette
            name = candidate
        ))

    fig.update_layout(
        title = f'Delegates earned from {state}',
        title_x = 0.5,
        xaxis_title = 'Candidates',
        yaxis_title = 'Delegates',
        yaxis = dict(dtick=50),
        xaxis = dict(dtick=1)
    )
    return fig



# run the app
app.run(debug=True)  