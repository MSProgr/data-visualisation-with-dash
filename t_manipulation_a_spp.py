import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import base64
import io

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

app = dash.Dash(__name__,external_scripts=external_scripts,external_stylesheets=external_stylesheets)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app.layout = html.Div(className='container',children=[
		html.H2("Editable DataTable"),
		dash_table.DataTable(id="data_table",
			columns=[{'id':c,'name':c,'selectable':True,'deletable':True,'renamable':True} for c in df.columns],
			data=df.to_dict('records'),
			filter_action='native',
			sort_mode='multi',
			sort_action='native',
			editable=True,
			page_current=0,
			page_size=10,
			page_action='native',
			column_selectable='multi',
			row_selectable='multi',
			selected_columns=[],
			selected_rows=[]),
		html.Br(),
		html.Br(),
		html.Br(),
		html.Div(id='feature_graph', className='row'),
		html.Br(),
		html.Br(),
		html.Br(),
		dcc.Upload(id='upload_input',
			children=[
				'Glissez le fichier ou',
				html.A("Selectionner le fichier")],
			style={
				'width': '100%', 'height': '60px', 'lineHeight': '60px',
				'borderWidth': '1px', 'borderStyle': 'dashed',
				'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
			}),
		html.Br(),
		html.Br(),
		html.Br(),
		dash_table.DataTable(id='display_upload_data',page_current=0,page_size=10,page_action='native',
			filter_action='native',sort_mode='multi',sort_action='native',editable=True),
		html.Br(),
		html.Br(),
		html.Br(),
		dcc.Graph(id="graph_upload_data")
	])

@app.callback(Output('feature_graph','children'),[
		Input('data_table','derived_virtual_data'),
		Input('data_table','derived_virtual_selected_rows')])
def show_graphs(dataset,selected_rows):
	if selected_rows is None:
		selected_rows = []

	dataframe = pd.DataFrame(dataset)

	colors = ['#E07F18' if i in selected_rows else '#0486FF' for i in range(len(dataframe))]
	return [
		html.Div(className='col-md-6 col-sm-6',children=[
		dcc.Graph(figure={
			'data':[{
				'x':dataframe['country'],
				'y':dataframe[col],
				'type':'bar',
				'marker':{'color':colors}
			}],
			'layout':{
				'xaxis':{'automargin':True,'title':'country'},
				'yaxis':{'automargin':True,'title':col},
				'margin':{'l':10,'r':10,'t':20}
			}
		})]) for col in ['pop','lifeExp','gdpPercap'] if col in dataframe.columns
	]

def parse_content(contents,filename):
	content_type,content_data = contents.split(",")
	decoded = base64.b64decode(content_data)

	if 'csv' in filename:
		return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
	elif 'xls' in filename:
		return pd.read_excel(io.BytesIO(decoded))

@app.callback([Output('display_upload_data','data'),Output('display_upload_data','columns')],
	[Input('upload_input','contents')],
	[State('upload_input','filename')])
def show_data(contents,filename):
	if contents is None:
		return [{}],[]
	dataframe=parse_content(contents,filename)
	data = dataframe.to_dict('records')
	cols = [{'id':c,'name':c,'deletable':True,'selectable':True,'renamable':True} for c in dataframe.columns]
	return data,cols

@app.callback(Output('graph_upload_data','figure'),
	[Input('display_upload_data','derived_virtual_data')])
def upload_data_graph(derived_virtual_data):
	dataframe = pd.DataFrame(derived_virtual_data)
	if dataframe.empty or len(dataframe.columns)<=1:
		return {
			'data':[{
				'x': [],
				'y': []
			}]
		}
	else:
		return {
			'data':[{
				'x':dataframe[dataframe.columns[0]],
				'y':dataframe[dataframe.columns[1]],
				'mode': 'markers',
                'marker': {'size': 12,'color':'#0780F1'},
                'showlegend':True,
			},
			{
				'x':dataframe[dataframe.columns[0]],
				'y':dataframe[dataframe.columns[2]],
				'mode': 'markers',
                'marker': {'size': 12,'color':'#E68C0A'},
                'showlegend':True,
			}]
		}

if __name__ == "__main__":
	app.run_server(debug=True)




