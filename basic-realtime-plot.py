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
                external_stylesheets=['static/main.css'],
                update_title=None)

figure_margin = go.layout.Margin(b=0, l=0, r=0, t=0)
live_update_graph_1 = dcc.Graph(id='live_update_graph_1',
                                animate=False,
                                style={'width': '100%'},
                                config={'displayModeBar': False,
                                        'staticPlot': True},
                                figure=go.Figure(go.Scatter(x=[], y=[], mode='lines'),
                                                 layout={'xaxis_title': "Time (s)",
                                                         'yaxis_title': "X",
                                                         'font': {'family': "Nunito, sans-serif",
                                                                  'size': 12},
                                                         'margin': figure_margin}))

app.layout = html.Div([
    html.Div([
        html.H2("Realtime display of Gaussian data"),
        live_update_graph_1,
        dcc.Interval(id='update_timer_1',
                     interval=REFRESH_RATE_MS)
    ], className='container vcontainer')
], className='page')


@app.callback(Output('live_update_graph_1', 'extendData'),
              Input('update_timer_1', 'n_intervals'))
def update_graph_1(n_intervals: int):
    new_x, new_y = generate_data()
    return {'x': [[new_x]],
            'y': [[new_y]]}, [0], None


if __name__ == '__main__':
    app.run_server(debug=True)
