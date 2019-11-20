from dash import Dash
from dash_table import DataTable
from dash.dependencies import Input,Output,State
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

app = Dash(__name__)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app.layout = html.Div(children=[
	DataTable(id='data-table-interactivity',
		columns=[{'id':c,'name':c,'deletable':True,'renamable':True,'selectable':True} for c in df.columns],
		data=df.to_dict('records'),
		editable=True,
		filter_action='native',
		sort_action='native',
		sort_mode='multi',
		column_selectable='multi',
		row_selectable='multi',
		selected_columns=[],
		selected_rows=[],
		row_deletable=True,
		page_action='native',
		page_current=0,
		page_size=10
		),
	html.Br(),
	html.Br(),
	html.Div(id='data_table_graph_container')
	])

@app.callback(Output('data-table-interactivity','style_data_conditional'),
	[Input('data-table-interactivity','selected_rows'),
	Input('data-table-interactivity','selected_columns')])
def update_style(selected_rows,selected_columns):
	a = [{
		'if':{'row_index':i},
		'background':'#4747F5'
		} for i in selected_rows]
	b = [{
		'if':{'column_id':i},
		'background':'#EE605C'
	}for i in selected_columns]

	return a+b


@app.callback(Output('data_table_graph_container','children'),
	[Input('data-table-interactivity','derived_virtual_data'),
	Input('data-table-interactivity','derived_virtual_selected_rows')])
def update_graph(the_data,derived_virtual_selected_rows):
	if derived_virtual_selected_rows is None:
		derived_virtual_selected_rows=[]

	dff = pd.DataFrame(the_data)

	colors = ['#F47C05' if i in derived_virtual_selected_rows else '#055CF4' for i in range(len(dff))]

	return [dcc.Graph(figure={
			'data':[{'x':dff['country'],
					'y':dff[col],
					'type':'bar',
					'marker':{'color':colors}}],
			'layout':{
				'xaxis':{'automargin':True,'title':'Country'},
				'yaxis':{'automargin':True,"title":col},
				'margin' : {'l':10,'r':10}
			}
		}) for col in {'pop','lifeExp'} if col in dff.columns]


if __name__ == "__main__":
	app.run_server(debug=True)