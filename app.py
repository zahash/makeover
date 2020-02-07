import dash
import dash_core_components as dcc
import dash_html_components as html

import os
import pandas as pd

from utils import generate_plots
from config import EXTERNAL_STYLESHEETS, EXTERNAL_SCRIPTS, DATA_DIR

app = dash.Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS,
                external_scripts=EXTERNAL_SCRIPTS)


dataset_name = 'churn_modelling.csv'
dataset_path = os.path.join(DATA_DIR, dataset_name)

df = pd.read_csv(dataset_path)
feat = df.drop(columns=["Exited"])
label = df["Exited"]
plots = generate_plots(feat, label)

title = html.H1(children=dataset_name, style={
    'textAlign': 'center', 'fontFamily': 'Montserrat'})

body_children = []
cols = []
for i, graph_obj in enumerate(plots):
    cols.append(html.Div(className='col-md-4', children=[graph_obj]))
    if (i+1) % 3 == 0:
        body_children.append(html.Div(className='row', children=cols))
        cols = []
body_children.append(html.Div(className='row', children=cols))


body = html.Div(children=body_children)
app.layout = html.Div(children=[title, body])

if __name__ == '__main__':
    app.run_server(debug=True)
