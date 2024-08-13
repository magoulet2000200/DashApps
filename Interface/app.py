import os

import dash
from dash import Dash, html


app = Dash(
    __name__,
    assets_folder='assets',
    external_stylesheets=[
        'https://codepen.io/chriddyp/pen/bWLwgP.css',
        # 'style.css',
    ],
    use_pages=True
)

app.layout = html.Div([
    html.H1(f'Sanuvox DashBoard [{os.environ.get("SIDE_ENV", "Local")}]', style={'textAlign': 'center'}),
    dash.page_container
])


if __name__ == '__main__':
    app.run_server(
        debug=True,
        host=os.environ.get('APP_IP', "127.0.0.1"),
        port=os.environ.get('APP_PORT', 8080),
        use_reloader=False
    )
