import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from  dash.dependencies import Input,Output,State
import pandas as pd
import base64
import io

external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.4.1.slim.min.js',
        'integrity': 'sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
        'integrity': 'sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js',
        'integrity': 'sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6',
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

app = dash.Dash(external_scripts=external_scripts,external_stylesheets=external_stylesheets)

app.layout = html.Div(className='container',children=[
    dcc.Upload(id='upload_space',children=[
        "please drag and drop a file or ",
        html.A("Select the file")
    ],
    style={'width':'100%','height':'60px','borderStyle':'dashed','textAlign':'center',
    'borderRadius':'5px','borderWidth':'1px','margin':'10px','lineHeight':'60px'}),
    dash_table.DataTable(id='data_container',editable=True,page_action='native',
    page_size=5,page_current=0,filter_action='native',sort_mode='multi',sort_action='native'),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Hr(style={'backgroundColor':'#F19209'}),
    html.Div(className='row',children=[

        html.Div(className='col-md-5 col-sm-5',children=[
            dcc.Dropdown(id='col_choice',
                placeholder='please select a column to plot by value counts'),
            html.Br(),
            dcc.Dropdown(id='graph_choice',
                placeholder='please select a a graph type to plot',
                options=[{'value':'pie','label':'pie'},{'value':'bar','label':'bar'}],
                value='bar'),
            html.Br(),
            dcc.Graph(id="graph_by_count"),
            html.Br()
        ]),

        html.Div(className='col-md-6 col-sm-6 ml-auto',children=[
            html.H3('Descriptive Statistique'),
            dash_table.DataTable(id='descriptive_table'),
            html.Hr(style={'backgroundColor':'#F19209'}),
            dash_table.DataTable(id='correlation'),
            html.Br()
        ])

    ]),
    html.Hr(style={'backgroundColor':'#F19209'}),
    html.Div(className='row',children=[
        html.Div(className='col-md-6 col-sm-6',children=[
            html.H3('variable correlation visualization'),
            dcc.Graph('my_heat_map'),
        ]),
        html.Div(className='col-md-5 col-sm-5',children=[
            dcc.Dropdown(id='var_name',
                placeholder='variable name',multi=True),
            dcc.Graph(id='var_plot')
        ])
        
    ])
])

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
    if columns is None:
        return []
    else:
        col_names = [c.get('name') for c in columns]
        return [{'label':c,'value':c} for c in col_names]


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
[Input('data_container','derived_virtual_data'),Input('col_choice','value'),Input('graph_choice','value')])
def plot_graph_by_count(data,value,type_gr):
    try:
        df = pd.DataFrame(data)
        occurences = df[value].value_counts()
        x_data,labels = occurences.index,occurences.index
        y_data,values = occurences.values,occurences.values
        if type_gr=='pie':
            return {
            'data':[{
                    'labels':labels,
                    'values':values,
                    'type':type_gr
                }]
            }
        else:
            return {
            'data':[{
                    'x':x_data,
                    'y':y_data,
                    'type':type_gr
                }]
            }
    except:
        return {
        'data':[{'x':[],'y':[],'type':type_gr}]
        }

@app.callback([Output('descriptive_table','data'),Output('descriptive_table','columns')],
    [Input('data_container','derived_virtual_data')])
def show_descriptive_statistique(virtual_data):
    try:
        df = pd.DataFrame(virtual_data).describe()
        ordered_cols = ["stat variables"]+df.columns.to_list()
        df["stat variables"] = df.index
        return df.round(4).to_dict('records'),[{'id':c,'name':c} for c in ordered_cols]
    except:
        return [{}],[]

@app.callback([Output('correlation','data'),Output('correlation','columns')],
    [Input('data_container','derived_virtual_data')])
def show_correlated_variables(virtual_data):
    try:
        df = pd.DataFrame(virtual_data).corr(method='pearson')
        ordered_cols = ["corr variables"]+df.columns.to_list()
        df['corr variables'] = df.index
        return df.round(4).to_dict('records'),[{'id':c,'name':c} for c in ordered_cols]
    except:
        return [{}],[]
        

@app.callback(Output('my_heat_map','figure'),
    [Input('correlation','data')])
def show_heat_map(data):
    try:
        df = pd.DataFrame(data)
        df.drop(columns=['corr variables'],inplace=True)
        return {
            'data':[{
                'x':df.columns,
                'y':df.columns,
                'z':df.values,
                'type':'heatmap',
                'colorbar':{"title": "Correlation"},
                'showscale':True
            }]
        }
    except:
        return {
            'data':[{'z':[],'type':'heatmap'}]
        }

@app.callback(Output('var_name','options'),
[Input('data_container','columns')])
def get_x_y_options_values(columns):
    if columns is None:
        return []
    else:
        col_names = [c.get('name') for c in columns]
        return [{'label':c,'value':c} for c in col_names]


@app.callback(Output('var_plot','figure'),
[Input('data_container','data'),
Input('var_name','value')])
def plot_x_by_y(data,variables):
    try:
        df = pd.DataFrame(data)
        return {
            'data':[{'x':df[variable].values,'y':variable,
            'mode': 'markers',
            'marker': {'size': 12}} for variable in variables]
        }
    except:
        return {}


if __name__ == '__main__':
    app.run_server(debug=True)