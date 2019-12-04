<<<<<<< HEAD
=======
from flask import Flask,render_template,url_for

>>>>>>> c98cbb3205d0b9a83b24c2c0762dd3868c9c9c97
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np


external_scripts = [
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

<<<<<<< HEAD
app = dash.Dash(external_scripts=external_scripts,external_stylesheets=external_stylesheets)
=======
server = Flask(__name__)

app = dash.Dash(__name__,server=server,routes_pathname_prefix='/dash/',
    external_scripts=external_scripts,external_stylesheets=external_stylesheets)

@server.route('/dash/pie')
def index():
    return render_template("index.html")
>>>>>>> c98cbb3205d0b9a83b24c2c0762dd3868c9c9c97

app.layout=html.Div(className="card col-md-5 ml-auto mt-3",children=[
            html.Div(id='first_graph',children=[
                dcc.Graph(id='graph'),
                dcc.Interval(id='the_interval',interval=1*3000,n_intervals=0)
            ]),
            html.P("bonjour le amies qdjhkfhkdjfsdkhgkdskjhdsjfh") 
])

@app.callback(Output('graph','figure'),
    [Input('the_interval','n_intervals')])
def update_graph(n_intervals):
    data = [
        {
            'values': [np.random.randint(low=100, high=200),np.random.randint(low=150, high=250)],
            'labels':["inscrits",'non-inscrits'],
            'type': 'pie',
            #'hole':0.5,
            'marker':{'colors':["#EE920D","#29910D"]}
        },
    ]

    return {
                'data': data,
                'layout': {
                    'title':"Client Orange Money",
                    'margin': {'l': 30,'r': 0,'b': 30,'t': 30}
                }
            }


if __name__ == '__main__':
    app.run_server(debug=True)