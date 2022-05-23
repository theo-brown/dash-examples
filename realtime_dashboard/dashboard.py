from time import time
from turtle import update
from typing import Tuple
import dash
import plotly.graph_objects as go
from dash import html
import numpy as np
from updating_plot import UpdatingPlot

start_time = time()

def generate_data() -> Tuple[Tuple[float], Tuple[float]]:
    return [time() - start_time], [np.random.normal()]


app = dash.Dash(__name__,
                external_stylesheets=['static/main.css'],
                update_title=None)

updating_plot = UpdatingPlot(app=app,
                             id_="updating_plot",
                             trace=go.Scatter(x=[], y=[], mode='lines'),
                             heading="Updating Plot")

app.layout = html.Div([updating_plot.div], className='page')

updating_plot.set_callback(generate_data)

if __name__ == '__main__':
    app.run_server(debug=True)
