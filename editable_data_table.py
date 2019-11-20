import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output

import pandas as pd

app = dash.Dash()
params = ['Weight', 'Torque', 'Width', 'Height','Efficiency', 'Power', 'Displacement']

app.layout = html.Div(children=[
	dash_table.DataTable(id='editable-table',
		columns=[{'id':'Model','name':'Model'}]+[{'id':p,'name':p,'deletable':True,'renamable':True} for p in params],
		data=[dict(Model=i,**{param:0 for param in params}) for i in range(1,10)],
		editable=True,
		filter_action='native',
		sort_action='native',
		sort_mode='multi',
		column_selectable='multi',
		row_selectable='multi',
		row_deletable=True,
		selected_rows=[],
		selected_columns=[],
		page_action='native',
		page_current=0,
		page_size=5),
	html.Br(),
	html.Br(),

	dcc.Graph(id='dispay-graph-output')

])

@app.callback(Output('dispay-graph-output','figure'),
	[Input('editable-table','derived_virtual_data')])
def plot_data(data):
	df = pd.DataFrame(data)
	return {
		'data':[{
			'dimensions':[{
				'label':c,
				'values':df[c]
			} for c in df.columns],
			'type':'parcoords'
		}]
	}


if __name__ == '__main__':
	app.run_server(debug=True)