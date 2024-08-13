import dash
from dash import html

dash.register_page(__name__, path='/')


layout = html.Div([
    html.H2('Please Select an option', style={'textAlign': 'center'}),
    html.Div([
        html.Div(
            children=html.A(html.Button(f"Odor-Wall", style={'width':'100%', 'height':'100%', 'font-size': '30px'}), href="/odor_wall/"),
            style={'width':'50%','height':'200px', 'float': 'left'},
        ),
        html.Div(
            children=html.A(html.Button(f"Coil Clean", style={'width':'100%', 'height':'100%', 'font-size': '30px'}), href="/coil_clean/"),
            style={'width':'50%','height':'200px', 'float': 'left'},
        ),
        # html.Div(
        #     children=html.A(html.Button(f"Bio-Wall", style={'width':'100%', 'height':'100%', 'font-size': '30px'}), href="/bio_wall/"),
        #     style={'width':'50%','height':'200px', 'float': 'left'},
        # ),
    ], style={'width': '90%', 'overflow': 'hidden', 'margin': '0% 5%'}),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"Config"), href="/config/"),
])
