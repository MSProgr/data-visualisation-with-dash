import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output, State
import dash_table

import pandas as pd
import numpy as np

import base64
import io

app=dash.Dash()

app.layout=html.Div(children=[
	dcc.Upload(id="data_upload",
		children=html.Div([
			'Drag and drop or ',
			html.A('Select a file')
		]),
		style={
				'width': '100%', 'height': '60px', 'lineHeight': '60px',
				'borderWidth': '1px', 'borderStyle': 'dashed',
				'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
		},
	),
	dash_table.DataTable(id="data_container",
		editable=True,
		column_selectable='multi',
		page_action='native',
		page_current=0,
		page_size=10),
	html.Br(),
	html.Br(),
	dcc.Graph(id='graph_container')
])

def parse_contents(contents,filename):
	content_type,content_string = contents.split(",")
	decoded = base64.b64decode(content_string)

	if 'csv' in filename:
		return pd.read_csv(io.StringIO(decoded.decode("utf-8")),error_bad_lines=False)
	elif 'xls' in filename:
		return pd.read_excel(io.BytesIO(decoded),error_bad_lines=False)

@app.callback([Output('data_container',"data"),
	Output('data_container','columns')],
	[Input('data_upload','contents')],
	[State('data_upload','filename')])
def output_data(contents,filename):
	if contents is None:
		return [{}],[]
	df = parse_contents(contents,filename)
	data = df.to_dict('records')
	cols = [{'id':c,'name':c,'selectable':True,'renamable':True,'deletable':True} for c in df.columns]
	return data,cols

@app.callback(Output('graph_container','figure'),
	[Input('data_container','derived_virtual_data')])
def display_graph(rows):
	df = pd.DataFrame(rows)
	cols = df.columns
	if df.empty or len(df.columns)<1:
		return {'data':[{
			'x':[],
			'y':[],
			'type':'bar'
		}]}

	return {
		'data':[{'x':df[cols[0]],'y':df[cols[1]],'type':'bar'}]
	}


if __name__ == '__main__':
    app.run_server(debug=True) 