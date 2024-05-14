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
# Prepare state dataframe (prim_county_results.csv)
df = pd.read_csv('prim_state_results.csv', dtype={'Delegates': int})
df['State Code'] = df['State'].map(us_state_to_code)
dem_winner_df = df.query("Party == 'Democratic' & Winner == 'Yes'")
rep_winner_df = df.query("Party == 'Republican' & Winner == 'Yes'")

# Prepare county dataframe (prim_state_results.csv)
df_county = pd.read_csv('prim_county_results.csv', dtype={'fips':str})
df_county['fips'] = df_county['fips'].str.zfill(5) # Filter out only the rows with 'fips' value

# Load GeoJSON  
with open('geojson-counties-fips.json') as response:
    geojson_data = json.load(response)


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
                                dcc.Graph(id='choropleth-map', clear_on_unhover=False)],
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
                                                dcc.Graph(id='us-graph')],
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
        
    fig = px.choropleth(
                party_df,
                locations = "State Code",
                color = "Delegates",
                color_continuous_scale = colorscale,
                locationmode = "USA-states"
    )

    fig.update_traces(
        hovertemplate = 
            '%{customdata[5]}<br><br>' +
            'Party: <i>%{customdata[0]}</i><br>' +
            'Winning Candidate: <i>%{customdata[1]}</i><br>' +
            'Votes: <i>%{customdata[2]}</i><br>' +
            'Incumbent: <i>%{customdata[3]}</i><br>' +
            'Delegates: <i>%{customdata[4]}</i>',
            customdata = party_df[['Party', 'Candidate', 'Vote', 'Incumbent', 'Delegates', 'State']],
    )

    fig.update_layout(
        geo = dict(scope="usa"),
        coloraxis_colorbar = dict(
        title = '',
        ticksuffix = "",
        tickprefix = "",
        len = 0.6,
        thickness = 10,  
        showticklabels = False
        )
    )
    
    return fig 
   


@app.callback(
    Output('us-graph', 'figure'),
    Input('choropleth-map', 'hoverData'),
    Input('party-dropdown', 'value')
)
def update_barchart(hoverData, selected_party):
    # Filter the data for the selected state and party
    if selected_party == 'democratic':
        state_data = df[df['Party'] == 'Democratic']
        all_state = dem_winner_df
        candidate_colors = ['#1f77b4', 'darkgoldenrod'] # Colours for Democratic legends
        colours = ['#1f77b4', '#6A5ACD', '#191970', '#4B0082', '#0F52BA']
      
    else:
        state_data = df[df['Party'] == 'Republican'] 
        all_state = rep_winner_df
        candidate_colors = ['#d62728', 'teal']    # Colours for Republican legends  
        colours = ['#d62728', '#800020', '#800000', '#CB4154', '#80461B']           
 

    if hoverData is None: # When cursor isn't hovering on any state
        fig_all = px.bar(
            all_state,
            x = "State",
            y = "Delegates",
            color = "Candidate",
            barmode = "relative",
            color_discrete_map = dict(zip(all_state['Candidate'].unique(), candidate_colors)) 
           
        )
       
        fig_all.update_traces(
            hovertemplate = 
                        '%{x}<br><br>' +
                        'Party: <i>%{customdata[0]}</i><br>' +
                        'Winning Candidate: <i>%{customdata[1]}</i><br>' +
                        'Delegates: <i>%{customdata[2]}</i><extra></extra>',
            customdata = all_state[['Party', 'Candidate', 'Delegates']]
        ) 

        fig_all.update_layout(
            title = 'Delegates earned from each state',
            title_x = 0.5,
            xaxis_title = 'State',
            yaxis_title = 'Delegates',
            yaxis = dict(dtick=50),
            xaxis = dict(dtick=1)
        )

        return fig_all
    


    # When cursor is on a state
    state = hoverData['points'][0]['customdata'][-1]
    state_data = state_data[state_data['State'] == state]

    fig = px.bar(
        state_data,
            x = "Candidate",
            y = "Delegates",
            barmode = "relative",
            color="Candidate",
            color_discrete_map = dict(zip(all_state['Candidate'].unique(), colours)) 
    )

    fig.update_traces(
        hovertemplate = 'State: <i>%{customdata[0]}<br><br>' +
                  'Party: <i>%{customdata[1]}</i><br>' +
                  'Candidate: <i>%{x}</i><br>' +
                  'Votes: <i>%{customdata[2]}</i><extra></extra>',
        customdata = state_data[['State', 'Party', 'Vote']]
)

    fig.update_layout(
        title = f'Delegates earned from {state}',
        title_x = 0.5,
        xaxis_title = 'Candidates',
        yaxis_title = 'Delegates',
        yaxis = dict(dtick=50),
        xaxis = dict(dtick=1)
    )
    return fig



@app.callback(
    Output('state-graph', 'figure'),
    Input('choropleth-map', 'hoverData'),
    Input('party-dropdown', 'value'))

def plot_state_map(hoverData, selected_party):
    if hoverData is None:
        # Return an empty figure if no state is hovered over
        return {}


    # Get the state name from the hoverData
    state = hoverData['points'][0]['customdata'][-1]

    # Filter the data for the selected state and party
    if selected_party == 'democratic':
        state_counties = df_county[(df_county['State'] == state) & (df_county['Party'] == 'Democratic')]
        state_data = df[df['Party'] == 'Democratic']
        state_data = state_data[state_data['State'] == state]
        colour = ['#1f77b4']
       
    else:
        state_counties = df_county[(df_county['State'] == state) & (df_county['Party'] == 'Republican')]
        state_data = df[df['Party'] == 'Remocratic']
        state_data = state_data[state_data['State'] == state]
        colour = ['#d62728']
    
    
    # Create boolean variable to check whether fips values exist for a state (1. Some missing values, 2. No missing values)
    have_fips_bool = ((state_counties['fips'].isnull()).any() and (state_counties['fips'].notnull()).any()) or state_counties['fips'].notnull().any()
    
    if have_fips_bool:
        # If county data is available, display the state area with county borderlines
        fig = px.choropleth(
            state_counties,
            geojson = geojson_data,
            color = 'State',
            locations = 'fips',
            color_discrete_sequence = colour
        )

        fig.update_traces(
            hovertemplate = 
                '%{customdata[0]} %{customdata[1]}<br><br>' +
                'Party: <i>%{customdata[2]}</i><br>' +
                'Winning Candidate: <i>%{customdata[3]}</i><br>' +
                'Votes: <i>%{customdata[4]}</i><br>', 
                customdata = state_counties[['State', 'County', 'Party', 'Candidate', 'Vote']],
            showlegend = False
        )
    
    else:
        # If county data is not available, display only the state area
        fig = px.choropleth(
            state_data,
            color = 'State',
            locations = "State Code",
            color_discrete_sequence = colour,
            locationmode = "USA-states"
        )
        
    fig.update_geos(fitbounds = "locations", visible = False)
    fig.update_layout(title=f'{state}',
                      title_x = 0.5)

    return fig



# run the app
app.run(debug=True)  