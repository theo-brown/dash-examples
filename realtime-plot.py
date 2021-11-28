import dash
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np
from collections import deque

NUM_POINTS = None
REFRESH_RATE_MS = 50

x_data = deque(maxlen=NUM_POINTS)
y_data = deque(maxlen=NUM_POINTS)

app = dash.Dash(__name__,
                external_stylesheets=['static/main.css'])

app.layout = html.Div([
    html.Div([
        html.H1("Realtime display of Gaussian data"),
        dcc.Graph(id='live-update-graph1',
                  animate=False,
                  config={'displayModeBar': False,
                          'staticPlot': True}),
        dcc.Interval(id='update-timer1',
                     interval=REFRESH_RATE_MS)
    ], className="container vcontainer content")
], className="container vcontainer page")


@app.callback(Output('live-update-graph1', 'figure'),
              Input('update-timer1', 'n_intervals'))
def update_graph(n_intervals: int) -> dict:
    x_data.append(x_data[-1] + 1 if x_data else 0)
    y_data.append(np.random.normal())

    return {'data': [go.Scatter(x=list(x_data),
                                y=list(y_data),
                                mode='lines')]}


if __name__ == '__main__':
    app.run_server(debug=True)
