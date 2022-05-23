from typing import Callable, Iterable, Tuple
import plotly
import plotly.basedatatypes
import dash


class UpdatingPlot():
    def __init__(self,
                 app : dash.Dash,
                 id_ : str,
                 trace : plotly.basedatatypes.BaseTraceType,
                 heading : str,
                 refresh_rate_ms : int = 50,
                 x_axis_title : str = '',
                 y_axis_title : str = '',
                 margin : dict = {'top': 0, 'bottom': 0, 'left': 0, 'right': 0},
                 fontsize : int = 12) -> None:
        self.id_ = id_
        self.app = app

        #
        # Assemble components
        #
        # Figure
        figure_margin = plotly.graph_objs.layout.Margin(t=margin['top'], b=margin['bottom'],
                                                        l=margin['left'], r=margin['right'])

        self.graph = dash.dcc.Graph(id=self.id_,
                                    animate=False,
                                    style={'width': '100%'},
                                    config={'displayModeBar': False,
                                            'staticPlot': True},
                                    figure=plotly.graph_objs.Figure(trace,
                                                                    layout={'xaxis_title': x_axis_title,
                                                                            'yaxis_title': y_axis_title,
                                                                            'font': {'family': "Nunito, sans-serif",
                                                                                    'size': fontsize},
                                                                            'margin': figure_margin}))

        # Timer
        self.timer = dash.dcc.Interval(id=f'{self.id_}_update_timer',
                                       interval=refresh_rate_ms)

        # Div
        self.div = dash.html.Div([dash.html.H3(heading),
                                  self.timer,
                                  self.graph],
                                 className='container vcontainer')

    def set_callback(self, get_new_data : Callable[[None], Tuple[Iterable, Iterable]]):
        self.get_new_data = get_new_data

        @self.app.callback(dash.dependencies.Output(self.graph.id, 'extendData'),
                           dash.dependencies.Input(self.timer.id, 'n_intervals'))
        def update(n_intervals: int):
           new_x_data, new_y_data = get_new_data() 
           return ({'x': [new_x_data],
                   'y': [new_y_data]}, # New data points
                   [0], # Trace to update
                   None) # max number points to update
