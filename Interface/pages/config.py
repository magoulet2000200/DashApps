import dash
from dash import html, dcc, callback, Output, Input, State

import configparser
from config import config_path


dash.register_page(__name__)

config = configparser.ConfigParser()
config.read(config_path)


layout = html.Div([
    html.H2(id="conf_title", children='Configuration', style={'textAlign': 'center'}),

    html.Form(children=[
        
        # html.Label("Printer Port", htmlFor="printer_port"),
        # dcc.Dropdown(id="printer_port", options=[]),

        html.P("", style={'height':'20px'}),
        html.Button("Update", id="update_config"),
    ]),
    html.P("", style={'height':'50px'}),
    html.A(html.Button(f"< Home"), href="/"),
    html.P(id='placeholder4'),
])


# @callback(
#     Output('printer_port', 'value'),
#     Output('printer_port', 'options'),
#     Input('update_config', 'n_clicks'),
#     State('printer_port', 'value'),
# )
# def _content(n_clicks, printer):
#     update = False
#     # port of the printer
#     # if printer is None:
#     #     update = True
#     #     printer = config['DEFAULT'].get("printer_port", "")
#     # elif config['DEFAULT'].get("printer_port", "") != printer:
#     #     update = True
#     #     config['DEFAULT']['printer_port'] = printer
#     # z = Zebra("ZTC-ZD421-300dpi-ZPL")
#     # printers = z.getqueues()
#     # update value if anything had changed
#     if update:
#         with open(config_path, 'w') as configfile:
#             config.write(configfile)
#     return printer, printers
