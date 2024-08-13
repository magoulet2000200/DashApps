import os
import dash
from dash import html, dcc, callback, Output, Input, State
import pandas as pd

import pint


ureg = pint.UnitRegistry()
ureg.load_definitions('./Interface/apps/data/custom_unit.txt')
Q_ = ureg.Quantity

import configparser
from config import config_path


dash.register_page(__name__, path='/process_1/')


config = configparser.ConfigParser()
config.read(config_path)


layout = html.Div([
    html.H2(children='Process 1', style={'textAlign': 'center'}),
    html.Div( children=[
        html.Div([
            html.Form(children=[
                html.Label("Air Flow"),
                html.Div([
                    dcc.Input(id="P1_air_flow_input", value=12000, type="number", placeholder="Air Flow", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="P1_air_flow_unit", value="CFM", options=["CFM", "CMH"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
            ]),
            html.Div([
                html.P("", style={'height':'50px'}),
                html.Button("Process >", id="P1_process"),
            ], style={'width': '100%', 'float': 'left'}),
        ], style={'width': '40%', 'float': 'left', 'margin': '0% 5%'}),

        html.Div(children=[
            dcc.Input(id='P1_result', readOnly=True, value="Set value and process them"),
        ], style={'width': '40%', 'float': 'right', 'margin': '0% 5%'}),

    ], style={'width': '100%', 'overflow': 'hidden'}),
    
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.A(html.Button(f"< Configuration"), href="/config/"),
])


@callback(
    Output('P1_air_flow_input', 'value'),
    State('P1_air_flow_input', 'value'),
    Input('P1_air_flow_unit', 'value'),
    prevent_initial_call=True,
)
def convert_air_flow(input, unit):
    try:
        if input is not None:
            if unit == "CFM":
                input = Q_(input, "CMH").to(unit)
            elif unit == "CMH":
                input = Q_(input, "CFM").to(unit)
        return input.magnitude
    except:
        return input



@callback(
    # Response
    Output('P1_result', 'value'),
    # air_flow
    State('P1_air_flow_input', 'value'),
    State('P1_air_flow_unit', 'value'),
    # INPUT
    Input('P1_process', 'n_clicks'),
    prevent_initial_call=True,
)
def convert_odor_concentration(af_i, af_u, n_click):
    # get air flow
    try:
        af = Q_(af_i, af_u)
    except Exception as e:
        return f"Air Flow: {e}", None, None, None
    
    try:
        1 / 0 # it will fail!
        return f"SUCCESS!"
    except Exception as e:
        return f"Failed: {e}"
