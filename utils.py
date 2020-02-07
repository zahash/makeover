import plotly.express as px
import plotly.graph_objs as go
import dash_core_components as dcc


def _get_numeric_categorical_columns(df):
    ''' 
    Finds out which columns are numeric and which
    are categorical in the given dataframe and 
    returns them as lists
    '''

    numeric_columns = []
    categorical_columns = []
    for col in df.columns:
        if df[col].dtype in [int, float]:
            if df[col].unique().shape[0] / df.shape[0] < 0.01:
                categorical_columns.append(col)
            else:
                numeric_columns.append(col)
        else:
            categorical_columns.append(col)

    return numeric_columns, categorical_columns


def generate_plots(df):
    '''
    returns a list of dcc.Graph objects
    '''
    numeric_columns, categorical_columns = _get_numeric_categorical_columns(df)

    plots = []
    for col in numeric_columns:
        fig = px.histogram(df, x=col, marginal='box', hover_data=df.columns)
        graph_obj = dcc.Graph(
            figure=fig
        )
        plots.append(graph_obj)

    for col in categorical_columns:

        categories, frequencies = zip(
            *sorted(df[col].value_counts().to_dict().items(), key=lambda x: x[1]))

        trace = go.Bar(
            x=list(frequencies),
            y=list(categories),
            orientation='h'
        )

        data = [trace]

        layout = go.Layout(
            title=col,
            xaxis=dict(title='freq'),
            yaxis=dict(title=col),
            hovermode='closest'
        )

        fig = go.Figure(data=data, layout=layout)
        graph_obj = dcc.Graph(
            figure=dict(data=data, layout=layout)
        )
        plots.append(graph_obj)

    return plots


# px.histogram(df, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=df.columns)
# px.bar(df, x="total_bill", y="day", orientation='h')

# import plotly.figure_factory as ff
# ff.create_distplot(hist_data)


# dcc.Graph(
#     id='petal-length-hist',
#     figure={
#         'data': [dict(
#             x=df['petal_length'][df['species'] == class_name],
#             type='histogram',
#             name=class_name
#         )for class_name in df['species'].unique()],
#         'layout': {
#             'title': 'Dash Data Visualization'
#         }
#     }
# )
