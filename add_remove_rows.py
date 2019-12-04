import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import dash_table

import pandas as pd
import numpy as np

app = dash.Dash()

if __name__ == '__main__':
	app.run_server(debug=True)