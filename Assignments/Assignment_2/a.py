import dash
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1('US Presidential Primary Election 2024'),
        html.Hr(),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='party-dropdown',
                    options=[
                        {'label': 'Democratic', 'value': 'democratic'},
                        {'label': 'Republican', 'value': 'republican'}
                    ],
                    value='democratic'
                ),
                dcc.Graph(id='choropleth-map')
            ], style={'width': '60%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div([
                html.Div([
                    html.H2('Graph 1'),
                    dcc.Graph(id='graph-1')
                ], style={'height': '50%'}),
                html.Div([
                    html.H2('Graph 2'),
                    dcc.Graph(id='graph-2')
                ], style={'height': '50%'})
            ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'top'})
        ], style={'display': 'flex'})
    ], style={'padding': '20px'})
])

if __name__ == '__main__':
    app.run_server(debug=True)