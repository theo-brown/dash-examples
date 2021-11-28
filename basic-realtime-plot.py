import dash
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np
from time import time


REFRESH_RATE_MS = 50
start_time = time()


def generate_data() -> (float, float):
    return time() - start_time, np.random.normal()


app = dash.Dash(__name__,
                external_stylesheets=['static/main.css'])

live_update_graph_1 = dcc.Graph(id='live_update_graph_1',
                                animate=False,
                                config={'displayModeBar': False,
                                        'staticPlot': True},
                                figure=go.Figure(go.Scatter(x=[], y=[], mode='lines')))

app.layout = html.Div([
    html.Div([
        html.H2("Realtime display of Gaussian data"),
        live_update_graph_1,
        dcc.Interval(id='update_timer_1',
                     interval=REFRESH_RATE_MS)
    ], className="container vcontainer content")
], className="container vcontainer page")


@app.callback(Output('live_update_graph_1', 'extendData'),
              Input('update_timer_1', 'n_intervals'))
def update_graph_1(n_intervals: int):
    new_x, new_y = generate_data()
    return dict(x=[[new_x]],
                y=[[new_y]]), [0], None


if __name__ == '__main__':
    app.run_server(debug=True)
