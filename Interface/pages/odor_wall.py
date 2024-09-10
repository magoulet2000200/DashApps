import os
import dash
from dash import html, dcc, callback, Output, Input, State
import pandas as pd
from API.sizing_api import Sizing_API

import pint
# from chemicals import CAS_from_any, MW

USERNAME = "admin@sanuvox.com"
PASSWORD = "sanuvox"

# TODO:
ureg = pint.UnitRegistry()
ureg.load_definitions('./Interface/apps/data/custom_unit.txt')
Q_ = ureg.Quantity

import configparser
from config import config_path


dash.register_page(__name__, path='/odor_wall/')


config = configparser.ConfigParser()
config.read(config_path)


side = os.environ.get("SIDE_ENV", "local")
api = Sizing_API(side=side, username=USERNAME, password=PASSWORD)
data = api.get_odor_list()
df = pd.DataFrame(data["odors"])
df["filter_name"] = (df["name"] + " ("+ df["cas_rn"] + ")")

layout = html.Div([
    html.H2(children='Odor Wall', style={'textAlign': 'center'}),
    html.Div(id="main_comm_view", children=[
        html.Div([
            html.Form(children=[
                html.Label("Odor"),
                html.Div([
                    dcc.Dropdown(id="OW_odor_choice", value=df["filter_name"].iloc[0], options=list(df["filter_name"]), style={'width': '80%', 'float': 'left'}),
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

                html.Label("Air Temperature"),
                html.Div([
                    dcc.Input(id="OW_temperature_input", type="number", value=25, placeholder="Temperature", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_temperature_unit", value="°C", options=["°C", "°F"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
                
                html.Label("Air Humidity (%)"),
                html.Div([
                    dcc.Input(id="OW_humidity_input", value=40, type="number", placeholder="Humidity (%)", style={'width': '20%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Odor Concentration"),
                html.Div([
                    dcc.Input(id="OW_concentration_input", type="number", value=10, placeholder="Concentration", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="OW_concentration_unit", value="ppm", options=["ppm", "ppb"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
            ]),
            html.Div([
                html.P("", style={'height':'50px'}),
                html.Button("Process", id="OW_process_odor"),
            ], style={'width': '100%', 'float': 'left'}),
        ], style={'width': '40%', 'float': 'left', 'margin': '0% 5%'}),

        html.Div(children=[
            dcc.Textarea(
                id='OW_resultResponse',
                readOnly=True,
                value="Set value and process them!",
                style={'width': '100%', 'height': 100},
            ),
        ], style={'width': '40%', 'float': 'right', 'margin': '0% 5%'}),

    ], style={'width': '100%', 'overflow': 'hidden'}),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.A(html.Button(f"Configuration >"), href="/config/"),
    html.P(id='OW_placeholder4'),
])


# @callback(
#     Output('OW_odor_choice', 'value'),
#     Output('OW_odor_choice', 'options'),
#     Input('OW_placeholder4', 'children'),
#     # prevent_initial_call=True,
# )
# def get_odor(style):
#     side = os.environ.get("SIDE_ENV", "local")
#     api = Sizing_API(side=side, username=USERNAME, password=PASSWORD)
#     data = api.get_odor_list()
#     df = pd.DataFrame(data["odors"])
#     return df["name"][0], list(df["name"])



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
        cas = df[df["filter_name"] == od]["cas_rn"].iloc[0]
    except Exception as e:
        return f"Could not retreive odor!"
    # get air flow
    try:
        af = Q_(af_i, af_u)
    except Exception as e:
        return f"Air Flow: {e}"
    # get vent height
    try:
        he = Q_(he_i, he_u)
    except Exception as e:
        return f"height: {e}"
    # get vent width
    try:
        wi = Q_(wi_i, wi_u)
    except Exception as e:
        return f"Width: {e}"
    # get temperature
    try:
        t = Q_(t_i, t_u)
    except Exception as e:
        return f"Temperature: {e}"
    # get humidity
    if hu_i < 0:
        return "Humidity must be over 0"
    elif hu_i > 100:
        return "Humidity can't be over 100"
    # get odor concentraion
    try:
        c = Q_(c_i, c_u)
    except Exception as e:
        return f"Temperature: {e}"
    # Test
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
        return f"SUCCESS: {resp['data']}"
    except:
        return f"FAILED: {resp}"
