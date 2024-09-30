import os
import dash
from dash import html, dcc, callback, Output, Input, State
import pandas as pd
import numpy as np
from API.sizing_api import Sizing_API

import plotly.express as px
import plotly.graph_objects as go

import pint

USERNAME = "user@sanuvox.com"
PASSWORD = "password"
PRICE_COLUMNS = {
    'product_number': 'Product Number', 
    'quantity': 'Quantity',
    'unit_price_CAD': 'Unit Price CAD',
    'unit_price_USD': 'Unit Price USD',
    'total_price_CAD': 'Total Price CAD',
    'total_price_USD': 'Total Price USD',
}
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
                    dcc.Input(id="CC_distance_input", value=20, type="number", placeholder="Distance", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_distance_unit", value="inch", options=["inch", "mm"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Air Temperature"),
                html.Div([
                    dcc.Input(id="CC_temperature_input", type="number", value=25, placeholder="Temperature", style={'width': '20%', 'float': 'left'}),
                    dcc.Dropdown(id="CC_temperature_unit", value="°C", options=["°C", "°F"], style={'width': '40%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
                
                html.Label("Is Downstream?"),
                html.Div([
                    dcc.Checklist(
                        ['Downstream', 'Auto-placement'], ['Downstream'],
                        id="CC_downstream",
                    )
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Row Numbers"),
                html.Div([
                    dcc.Input(id="CC_rows_input", type="number", value=1, min=1, placeholder="Rows", style={'width': '20%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),

                html.Label("Column Numbers"),
                html.Div([
                    dcc.Input(id="CC_columns_input", type="number", value=1, min=1, placeholder="Columns", style={'width': '20%', 'float': 'left'}),
                ], style={'width': '100%', 'float': 'left'}),
            ]),
            html.Div([
                html.P("", style={'height':'50px'}),
                html.Button("Process", id="CC_process"),
            ], style={'width': '100%', 'float': 'left'}),
        ], style={'width': '30%', 'float': 'left', 'margin': '0% 5%'}),

        html.Div(id="resultDiv", children=[
            dcc.Textarea(
                id='CC_resultResponse', readOnly=True,
                value="Set value and process them!",
                style={'width': '100%', 'height': 100},
            ),
            dash.dash_table.DataTable(columns=[{"id": i, "name": v} for i, v in PRICE_COLUMNS.items()], id="CC_table_price"),
            dcc.Graph(id="CC_graph_irr_coil"),
            dcc.Graph(id="CC_graph_dis_coil"),
            dcc.Graph(id="CC_graph_lamp_pos"),
        ], style={'width': '50%', 'float': 'right', 'margin': '0% 5%'}),

    ], style={'width': '100%', 'overflow': 'hidden'}),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.A(html.Button(f"Configuration >"), href="/config/"),
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
    Output("CC_graph_irr_coil", "figure"),
    Output("CC_graph_dis_coil", "figure"),
    Output("CC_graph_lamp_pos", "figure"),
    Output("CC_table_price", "data"),
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
    # row
    State('CC_rows_input', 'value'),
    # column
    State('CC_columns_input', 'value'),
    # INPUT
    Input('CC_process', 'n_clicks'),
    prevent_initial_call=True,
)
def convert_odor_concentration(af_i, af_u, he_i, he_u, wi_i, wi_u, dist_i, dist_u, t_i, t_u, do_i, r_n, c_n, n_click):
    # get air flow
    try:
        af = Q_(af_i, af_u)
    except Exception as e:
        return f"Air Flow: {e}", None, None, None, None
    # get vent height
    try:
        he = Q_(he_i, he_u)
    except Exception as e:
        return f"height: {e}", None, None, None, None
    # get vent width
    try:
        wi = Q_(wi_i, wi_u)
    except Exception as e:
        return f"Width: {e}", None, None, None, None
    # get coil distance
    try:
        dist = Q_(dist_i, dist_u)
    except Exception as e:
        return f"Width: {e}", None, None, None, None
    # get temperature
    try:
        t = Q_(t_i, t_u)
    except Exception as e:
        return f"Temperature: {e}", None, None, None, None
    # get humidity
    downstream = 'Downstream' in do_i
    auto = 'Auto-placement' in do_i
    # Test
    side = os.environ.get("SIDE_ENV", "local")
    api = Sizing_API(side=side, username=USERNAME, password=PASSWORD)
    try:
        resp = api.post_coil_clean(data={
            "air_flow": f"{af}",
            "height": f"{he}",
            "width": f"{wi}",
            "distance": f"{dist}",
            "air_temperature": f"{t}",
            "downstream": downstream,
            "auto_placement": auto,
            "row_nb": r_n,
            "column_nb": c_n,
        })
        data = resp['data']
        irr = np.array(data.pop('irridiance_matrix'))

        res = 800
        if he_i < wi_i:
            height_ratio = int(res * (he_i/wi_i))
            width_ratio  = res
            # Adjust Height
            if height_ratio < 230:
                height_ratio = 230
        else:
            height_ratio = res
            width_ratio  = int(res * (wi_i/he_i))
            # Adjust Width
            if width_ratio < 230:
                width_ratio = 230

        index = pd.Series(range(0, 50))* (he_i/50.0)
        columns = pd.Series(range(0, 50)) * (wi_i/50.0)
        df = pd.DataFrame(
            data=irr,
            index=index,
            columns=columns,
        )
        # TODO: arrange ratio problem
        sh_0, sh_1 = df.shape
        y, x = np.linspace(0, he_i, sh_0), np.linspace(0, wi_i, sh_1)
        z = df.values
        fig1 = go.Figure(
            data=go.Heatmap(
                z=z, x=x, y=y,
                colorbar={
                    "title": "uW/cm2",
                },
                zsmooth='best',
                hoverongaps=False,
                colorscale=[
                    [0,     "red"],
                    [0.100, "orange"],
                    [0.250, "green"],
                    [0.300, "darkgreen"],
                    [0.700, "blue"],
                    [1.000, "white"],
                ],
                zmin=0, zmax=1000,
            ),
            layout=go.Layout(
                title="Irradiance At Coil Surface",
                width=width_ratio, height=height_ratio,
            )
        )
        fig1.update_layout(
            xaxis_title="Width (Inch)",
            yaxis_title="Height (Inch)",
        )
        lamps = data.pop("lamps_position_matrix")
        lamp_len = data["lamp_length"].split()
        # Add shapes
        for lamp in lamps:
            x0 = lamp[0]
            y0 = lamp[1]
            fig1.add_shape(type="line",
                x0=x0, y0=y0, x1=x0+float(lamp_len[0]), y1=y0,
                line=dict(color="darkviolet", width=5)
            )

        df_z = (df > 250).map(lambda x: 1 if x else 0)
        perc = df_z.sum().sum() / (df_z.shape[0] * df_z.shape[1])

        z = df_z.values
        fig2 = go.Figure(
            data=go.Heatmap(
                z=z, x=x, y=y,
                colorbar={"title": "{:.0%}".format(perc)},
                zsmooth='best',
                hoverongaps=False,
                colorscale=[
                    [0,     "dimgray"],
                    [1.000, "aqua"],
                ],
                zmin=0, zmax=1,
            ),
            layout=go.Layout(
                title="Irradiance over 250 mW/cm2 At Coil Surface",
                width=width_ratio, height=height_ratio)
        )
        fig2.update_layout(
            xaxis_title="Width (Inch)",
            yaxis_title="Height (Inch)",
        )

        # price table
        pricing = data.pop('pricing')
        total_CAD = 0
        total_USD = 0
        for i in range(len(pricing)):
            total_CAD += pricing[i]['total_price_CAD']
            pricing[i]['unit_price_CAD'] = "${:,.2f} CAD".format(pricing[i]['unit_price_CAD'])
            pricing[i]['total_price_CAD'] = "${:,.2f} CAD".format(pricing[i]['total_price_CAD'])
            total_USD += float(pricing[i]['total_price_USD'])
            pricing[i]['unit_price_USD'] = "${:,.2f} USD".format(pricing[i]['unit_price_USD'])
            pricing[i]['total_price_USD'] = "${:,.2f} USD".format(pricing[i]['total_price_USD'])
        pricing.append({
            "product_number": "Total",
            "total_price_CAD": "${:,.2f} CAD".format(total_CAD),
            "total_price_USD": "${:,.2f} USD".format(total_USD),
        })

        return f"SUCCESS: {data}", fig1, fig2, None, pricing
    except Exception as e:
        return f"FAILED: {e}", None, None, None, None
