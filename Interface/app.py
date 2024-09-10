import os

import dash
from dash import Dash, html

dash_app = Dash(
    __name__,
    assets_folder='assets',
    external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        # 'style.css',
    ],
    use_pages=True
)

dash_app.layout = html.Div([
    html.H1(f'Sanuvox Sizing [{os.environ.get("SIDE_ENV", "Local")}]', style={'textAlign': 'center'}),
    dash.page_container
])


if __name__ == '__main__':
    dash_app.run_server(
        debug=True,
        threaded=True,
        host=os.environ.get('APP_IP', "127.0.0.1"),
        port=os.environ.get('APP_PORT', 8080),
        use_reloader=False
    )
