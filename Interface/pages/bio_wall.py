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


dash.register_page(__name__, path='/bio_wall/')


config = configparser.ConfigParser()
config.read(config_path)


df = pd.read_csv("./Interface/apps/data/c_threshold.csv")
layout = html.Div([
    html.H2(children='Odor Wall', style={'textAlign': 'center'}),
    html.Div(children=[
        html.Div([
            html.Form(children=[
                html.Label("Odor"),
                html.Div([
                    dcc.Dropdown(id="BW_odor_choice", options=list(df["name"]), style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Air Flow"),
                html.Div([
                    dcc.Input(id="BW_air_flow_input", type="number", placeholder="Air Flow", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="BW_air_flow_unit", value="CFM", options=["CFM", "CMH"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Duct Height"),
                html.Div([
                    dcc.Input(id="BW_height_input", type="number", placeholder="Height", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="BW_height_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Duct Width"),
                html.Div([
                    dcc.Input(id="BW_width_input", type="number", placeholder="Width", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="BW_width_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                # "air_temperature": "20 degC",
                html.Label("Air Temperature"),
                html.Div([
                    dcc.Input(id="BW_temperature_input", type="number", value=20, placeholder="Temperature", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="BW_temperature_unit", value="°C", options=["°C", "°F"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
                
                # "humidity": 40,
                html.Label("Air Humidity (%)"),
                html.Div([
                    dcc.Input(id="BW_humidity_input", value=40, type="number", placeholder="Humidity (%)", style={'width': '20%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                # "odor_concentration": "13 ppm",
                html.Label("Odor Concentration"),
                html.Div([
                    dcc.Input(id="BW_concentration_input", type="number", value=0, placeholder="Concentration", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="BW_concentration_unit", value="ppm", options=["ppm", "ppb"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
            ]),
            html.Div([
                html.P("", style={'height':'50px'}),
                html.Button("Process", id="BW_process_odor"),
            ], style={'width': '100%', 'float': 'left'}),
        ], style={'width': '40%', 'float': 'left', 'margin': '0% 5%'}),

        html.Div(children=[
            dcc.Input(id='BW_resultResponse', readOnly=True, value="Set value and process them"),
            dcc.Input(id='BW_resultLamps', readOnly=True, value="Number of lamps"),
            dcc.Input(id='BW_resultLamp', readOnly=True, value="Lamp lenght"),
            dcc.Input(id='BW_resultResOz', readOnly=True, value="Residual Ozone"),
        ], style={'width': '40%', 'float': 'right', 'margin': '0% 5%'}),

    ], style={'width': '100%', 'overflow': 'hidden'}),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.A(html.Button(f"Configuration >"), href="/config/"),
    html.P(id='BW_placeholder4'),
])


@callback(
    Output('BW_air_flow_input', 'value'),
    State('BW_air_flow_input', 'value'),
    Input('BW_air_flow_unit', 'value'),
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
    Output('BW_height_input', 'value'),
    State('BW_height_input', 'value'),
    Input('BW_height_unit', 'value'),
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
    Output('BW_width_input', 'value'),
    State('BW_width_input', 'value'),
    Input('BW_width_unit', 'value'),
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
    Output('BW_temperature_input', 'value'),
    State('BW_temperature_input', 'value'),
    Input('BW_temperature_unit', 'value'),
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
    Output('BW_concentration_input', 'value'),
    State('BW_concentration_input', 'value'),
    Input('BW_concentration_unit', 'value'),
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
    Output('BW_resultResponse', 'value'),
    Output('BW_resultLamps', 'value'),
    Output('BW_resultLamp', 'value'),
    Output('BW_resultResOz', 'value'),
    # odor
    State('BW_odor_choice', 'value'),
    # air_flow
    State('BW_air_flow_input', 'value'),
    State('BW_air_flow_unit', 'value'),
    # height
    State('BW_height_input', 'value'),
    State('BW_height_unit', 'value'),
    # width
    State('BW_width_input', 'value'),
    State('BW_width_unit', 'value'),
    # temperature
    State('BW_temperature_input', 'value'),
    State('BW_temperature_unit', 'value'),
    # humidity
    State('BW_humidity_input', 'value'),
    # concentration
    State('BW_concentration_input', 'value'),
    State('BW_concentration_unit', 'value'),
    
    Input('BW_process_odor', 'n_clicks'),
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
    USERNAME = "magoulet@sanuvox.com"
    PASSWORD = "S@nuv0x!"
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
