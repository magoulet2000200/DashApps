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


dash.register_page(__name__, path='/odor_wall/')


config = configparser.ConfigParser()
config.read(config_path)


df = pd.read_csv("./Interface/apps/data/c_threshold.csv")
layout = html.Div([
    html.H2(children='Odor Wall', style={'textAlign': 'center'}),
    html.Div(id="main_comm_view", children=[
        html.Div([
            html.Form(children=[
                html.Label("Odor"),
                html.Div([
                    dcc.Dropdown(id="OW_odor_choice", value=df["name"].iloc[0], options=list(df["name"]), style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Air Flow"),
                html.Div([
                    dcc.Input(id="OW_air_flow_input", value=12000, type="number", placeholder="Air Flow", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_air_flow_unit", value="CFM", options=["CFM", "CMH"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Duct Height"),
                html.Div([
                    dcc.Input(id="OW_height_input", value=64, type="number", placeholder="Height", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_height_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Duct Width"),
                html.Div([
                    dcc.Input(id="OW_width_input", value=64, type="number", placeholder="Width", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_width_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                # "air_temperature": "25 degC",
                html.Label("Air Temperature"),
                html.Div([
                    dcc.Input(id="OW_temperature_input", type="number", value=25, placeholder="Temperature", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_temperature_unit", value="°C", options=["°C", "°F"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
                
                # "humidity": 40,
                html.Label("Air Humidity (%)"),
                html.Div([
                    dcc.Input(id="OW_humidity_input", value=40, type="number", placeholder="Humidity (%)", style={'width': '20%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                # "odor_concentration": "12 ppm",
                html.Label("Odor Concentration"),
                html.Div([
                    dcc.Input(id="OW_concentration_input", type="number", value=0, placeholder="Concentration", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_concentration_unit", value="ppm", options=["ppm", "ppb"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
            ]),
            html.Div([
                html.P("", style={'height':'50px'}),
                html.Button("Process", id="OW_process_odor"),
            ], style={'width': '100%', 'float': 'left'}),
        ], style={'width': '40%', 'float': 'left', 'margin': '0% 5%'}),

        html.Div(children=[
            dcc.Input(id='OW_resultResponse', readOnly=True, value="Set value and process them"),
            dcc.Input(id='OW_resultLamps', readOnly=True, value="Number of lamps"),
            dcc.Input(id='OW_resultLamp', readOnly=True, value="Lamp lenght"),
            dcc.Input(id='OW_resultResOz', readOnly=True, value="Residual Ozone"),
        ]),#, style={'width': '40%', 'float': 'right', 'margin': '0% 5%'}),

    ], style={'width': '100%', 'overflow': 'hidden'}),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.A(html.Button(f"Configuration >"), href="/config/"),
    html.P(id='OW_placeholder4'),
])


@callback(
    Output('OW_air_flow_input', 'value'),
    State('OW_air_flow_input', 'value'),
    Input('OW_air_flow_unit', 'value'),
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
    Output('OW_height_input', 'value'),
    State('OW_height_input', 'value'),
    Input('OW_height_unit', 'value'),
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
    Output('OW_width_input', 'value'),
    State('OW_width_input', 'value'),
    Input('OW_width_unit', 'value'),
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
    Output('OW_temperature_input', 'value'),
    State('OW_temperature_input', 'value'),
    Input('OW_temperature_unit', 'value'),
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
    Output('OW_concentration_input', 'value'),
    State('OW_concentration_input', 'value'),
    Input('OW_concentration_unit', 'value'),
    prevent_initial_call=True,
)
def convert_odor_concentration(input, unit):
    try:
        if input is not None:
            if unit == "ppm":
                input = Q_(input, "ppb").to(unit)
            elif unit == "ppb":
                input = Q_(input, "ppm").to(unit)
        return input.magnitude
    except:
        return input


@callback(
    # Response
    Output('OW_resultResponse', 'value'),
    Output('OW_resultLamps', 'value'),
    Output('OW_resultLamp', 'value'),
    Output('OW_resultResOz', 'value'),
    # odor
    State('OW_odor_choice', 'value'),
    # air_flow
    State('OW_air_flow_input', 'value'),
    State('OW_air_flow_unit', 'value'),
    # height
    State('OW_height_input', 'value'),
    State('OW_height_unit', 'value'),
    # width
    State('OW_width_input', 'value'),
    State('OW_width_unit', 'value'),
    # temperature
    State('OW_temperature_input', 'value'),
    State('OW_temperature_unit', 'value'),
    # humidity
    State('OW_humidity_input', 'value'),
    # concentration
    State('OW_concentration_input', 'value'),
    State('OW_concentration_unit', 'value'),
    
    Input('OW_process_odor', 'n_clicks'),
    prevent_initial_call=True,
)
def convert_odor_concentration(od, af_i, af_u, he_i, he_u, wi_i, wi_u, t_i, t_u, hu_i, c_i, c_u, n_click):
    # get CAS
    try:
        cas = df[df["name"] == od]["cas_rn"].iloc[0]
    except Exception as e:
        return f"Could not retreive odor!", None, None, None
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
    # get temperature
    try:
        t = Q_(t_i, t_u)
    except Exception as e:
        return f"Temperature: {e}", None, None, None
    # get humidity
    if hu_i < 0:
        return "Humidity must be over 0", None, None, None
    elif hu_i > 100:
        return "Humidity can't be over 100", None, None, None
    # get odor concentraion
    try:
        c = Q_(c_i, c_u)
    except Exception as e:
        return f"Temperature: {e}", None, None, None
    # Test
    USERNAME = "admin@sanuvox.com"
    PASSWORD = "sanuvox"
    side = os.environ.get("SIDE_ENV", "local")
    api = Sizing_API(side=side, username=USERNAME, password=PASSWORD)
    resp = api.post_odor_wall(data={
        "cas_rn": cas,
        "air_flow": f"{af}",
        "height": f"{he}",
        "width": f"{wi}",
        "odor_concentration": f"{c}",
        "air_temperature": f"{t}",
        "humidity": hu_i,
    })
    try:
        return f"SUCCESS!", f"{resp['data']['required_lamps']} lamps", resp['data']['lamp_length'], resp['data']['residual_ozone']
    except:
        return f"Failed: {resp}", None, None, None
