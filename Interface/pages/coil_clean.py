import os
import dash
from dash import html, dcc, callback, Output, Input, State
import pandas as pd
from API.sizing_api import Sizing_API

import pint
# from chemicals import CAS_from_any, MW

# TODO:
ureg = pint.UnitRegistry()
ureg.load_definitions('./Interface/apps/data/custom_unit.txt')
Q_ = ureg.Quantity

import configparser
from config import config_path


dash.register_page(__name__, path='/coil_clean/')


config = configparser.ConfigParser()
config.read(config_path)


df = pd.read_csv("./Interface/apps/data/c_threshold.csv")
layout = html.Div([
    html.H2(children='Coil Clean', style={'textAlign': 'center'}),
    html.Div( children=[
        html.Div([
            html.Form(children=[

                html.Label("Air Flow"),
                html.Div([
                    dcc.Input(id="CC_air_flow_input", value=35000, type="number", placeholder="Air Flow", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_air_flow_unit", value="CFM", options=["CFM", "CMH"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Duct Height"),
                html.Div([
                    dcc.Input(id="CC_height_input", value=80, type="number", placeholder="Height", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_height_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Duct Width"),
                html.Div([
                    dcc.Input(id="CC_width_input", value=144, type="number", placeholder="Width", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_width_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Coil Distance"),
                html.Div([
                    dcc.Input(id="CC_distance_input", value=20, type="number", placeholder="Width", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_distance_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Air Temperature"),
                html.Div([
                    dcc.Input(id="CC_temperature_input", type="number", value=25, placeholder="Temperature", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_temperature_unit", value="°C", options=["°C", "°F"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
                
                html.Label("Is Downstream?"),
                html.Div([
                    # dcc.Input(id="CC_downstream", value=40, type="number", placeholder="Humidity (%)", style={'width': '20%', 'float': 'left'}),
                    dcc.Checklist(
                        ['Downstream',],
                        ['Downstream',],
                        id="CC_downstream",
                    )
                ], style={'width': '100%', 'float': 'left'}),
            ]),
            html.Div([
                html.P("", style={'height':'50px'}),
                html.Button("Process", id="CC_process"),
            ], style={'width': '100%', 'float': 'left'}),
        ], style={'width': '40%', 'float': 'left', 'margin': '0% 5%'}),

        html.Div(id="resultDiv", children=[
            dcc.Input(id='CC_resultResponse', readOnly=True, value="Set value and process them"),
            # dcc.Input(id='CC_resultLamps', readOnly=True, value="Number of lamps"),
            # dcc.Input(id='CC_resultLamp', readOnly=True, value="Lamp lenght"),
            # dcc.Input(id='CC_resultResOz', readOnly=True, value="Residual Ozone"),
        ], style={'width': '40%', 'float': 'right', 'margin': '0% 5%'}),

    ], style={'width': '100%', 'overflow': 'hidden'}),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.A(html.Button(f"Configuration >"), href="/config/"),
    html.P(id='CC_placeholder4'),
])


@callback(
    Output('CC_air_flow_input', 'value'),
    State('CC_air_flow_input', 'value'),
    Input('CC_air_flow_unit', 'value'),
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
    Output('CC_height_input', 'value'),
    State('CC_height_input', 'value'),
    Input('CC_height_unit', 'value'),
    prevent_initial_call=True,
)
def convert_height(input, unit):
    try:
        if input is not None:
            if unit == "inch":
                input = Q_(input, "mm").to(unit)
            elif unit == "mm":
                input = Q_(input, "inch").to(unit)
        return input.magnitude
    except:
        return input


@callback(
    Output('CC_width_input', 'value'),
    State('CC_width_input', 'value'),
    Input('CC_width_unit', 'value'),
    prevent_initial_call=True,
)
def convert_width(input, unit):
    try:
        if input is not None:
            if unit == "inch":
                input = Q_(input, "mm").to(unit)
            elif unit == "mm":
                input = Q_(input, "inch").to(unit)
        return input.magnitude
    except:
        return input
    
@callback(
    Output('CC_distance_input', 'value'),
    State('CC_distance_input', 'value'),
    Input('CC_distance_unit', 'value'),
    prevent_initial_call=True,
)
def convert_width(input, unit):
    try:
        if input is not None:
            if unit == "inch":
                input = Q_(input, "mm").to(unit)
            elif unit == "mm":
                input = Q_(input, "inch").to(unit)
        return input.magnitude
    except:
        return input


@callback(
    Output('CC_temperature_input', 'value'),
    State('CC_temperature_input', 'value'),
    Input('CC_temperature_unit', 'value'),
    prevent_initial_call=True,
)
def convert_temperature(input, unit):
    try:
        if input is not None:
            if unit == "°C":
                input = Q_(input, "degF").to("degC")
            elif unit == "°F":
                input = Q_(input, "degC").to("degF")
        return input.magnitude
    except:
        return input


@callback(
    # Response
    Output('CC_resultResponse', 'value'),
    # air_flow
    State('CC_air_flow_input', 'value'),
    State('CC_air_flow_unit', 'value'),
    # height
    State('CC_height_input', 'value'),
    State('CC_height_unit', 'value'),
    # width
    State('CC_width_input', 'value'),
    State('CC_width_unit', 'value'),
    # distance
    State('CC_distance_input', 'value'),
    State('CC_distance_unit', 'value'),
    # temperature
    State('CC_temperature_input', 'value'),
    State('CC_temperature_unit', 'value'),
    # humidity
    State('CC_downstream', 'value'),
    # INPUT
    Input('CC_process', 'n_clicks'),
    prevent_initial_call=True,
)
def convert_odor_concentration(af_i, af_u, he_i, he_u, wi_i, wi_u, dist_i, dist_u, t_i, t_u, do_i, n_click):
    # get air flow
    try:
        af = Q_(af_i, af_u)
    except Exception as e:
        return f"Air Flow: {e}", None, None, None
    # get vent height
    try:
        he = Q_(he_i, he_u)
    except Exception as e:
        return f"height: {e}", None, None, None
    # get vent width
    try:
        wi = Q_(wi_i, wi_u)
    except Exception as e:
        return f"Width: {e}", None, None, None
    # get coil distance
    try:
        dist = Q_(dist_i, dist_u)
    except Exception as e:
        return f"Width: {e}", None, None, None
    # get temperature
    try:
        t = Q_(t_i, t_u)
    except Exception as e:
        return f"Temperature: {e}", None, None, None
    # get humidity
    print(f"do_i: {do_i}")
    downstream = False
    # if do_i < 0:
    #     return "Humidity must be over 0", None, None, None
    # elif do_i > 100:
    #     return "Humidity can't be over 100", None, None, None
    # Test
    USERNAME = "admin@sanuvox.com"
    PASSWORD = "sanuvox"
    side = os.environ.get("SIDE_ENV", "local")
    api = Sizing_API(side=side, username=USERNAME, password=PASSWORD)
    resp = api.post_coil_clean(data={
        # TODO: Select virus
        "air_flow": f"{af}",
        "height": f"{he}",
        "width": f"{wi}",
        "distance": f"{dist}",
        "air_temperature": f"{t}",
        # "downstream": downstream,
    })
    try:
        return f"SUCCESS!"
    except:
        return f"Failed: {resp}"
