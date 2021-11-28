import dash
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd


app = dash.Dash(__name__,
                external_stylesheets=['static/main.css'])

figure1 = go.Figure()
figure1.add_scatter(name='gaussian_data')

data = pd.DataFrame()

app.layout = html.Div([
    html.Div([
        html.H1("Realtime display of Gaussian data"),
        dcc.Graph(id='live-update-graph1', figure=figure1),
        dcc.Interval(id='update-timer1',
                     interval=500)  # interval in ms
    ], className="container vcontainer content")
], className="container vcontainer page")


@app.callback(Output('live-update-graph1', 'figure'),
              Input('update-timer1', 'n_intervals'))
def update_graph(n_intervals: int) -> go.Figure:
    figure1.update_traces(x=[n_intervals],
                          y=[np.random.normal()],
                          selector={'name': 'gaussian_data'})
    return figure1

if __name__ == '__main__':
    app.run_server(debug=True)
