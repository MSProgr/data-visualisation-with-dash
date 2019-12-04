import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from  dash.dependencies import Input,Output,State
import pandas as pd
import base64
import io

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Upload(id='upload_space',children=[
        "please drag and drop a file or ",
        html.A("Select the file")
    ],
    style={'width':'100%','height':'60px','borderStyle':'dashed','textAlign':'center',
    'borderRadius':'5px','borderWidth':'1px','margin':'10px','lineHeight':'60px'}),
    dash_table.DataTable(id='data_container',editable=True,page_action='native',
    page_size=10,page_current=0,filter_action='native',sort_mode='multi',sort_action='native'),
    html.Br(),html.Br(),html.Br(),
    dcc.Dropdown(id='col_choice'),
    dcc.Graph(id="graph_by_count")
    ]
)

def parse_content(contents,filename):
    content_type,content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        return pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    elif 'xls' in filename:
        return pd.read_excel(io.BytesIO(decoded))

@app.callback(Output('col_choice','options'),
[Input('data_container','columns')])
def find_columns(columns):
    if columns is not None:
        col_names = [c.get('name') for c in columns]
        return [{'label':c,'value':c} for c in col_names]
    else:
        return [{}]


@app.callback([Output('data_container','data'),Output('data_container','columns')],
[Input('upload_space','contents')],[State('upload_space','filename')])
def show_contents(contents,filename):
    if contents is None:
        return [{}],[]
    else:
        df = parse_content(contents,filename)
        return df.to_dict('records'),[{'id':c,'name':c,'deletable':True,
                                    'renamable':True,'editable':True} for c in df.columns]

@app.callback(Output('graph_by_count','figure'),
[Input('data_container','data'),Input('col_choice','value')])
def plot_graph_by_count(data,value):
    if data is not None and value is not None:
        df = pd.DataFrame(data)
        occurences = df[value].value_counts()
        x_data = occurences.index
        y_data = occurences.values
        return {
        'data':[{
                'x':x_data,
                'y':y_data,
                'type':'bar'
            }]
        }
    else:
        return {
        'data':[{'x':[],'y':[],'type':'bar'}]
        }


if __name__ == '__main__':
    app.run_server(debug=True)
