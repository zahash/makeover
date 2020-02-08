import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import dash_core_components as dcc

import pandas as pd


def _get_numeric_categorical_columns(feat):
    ''' 
    Finds out which columns are numeric and which
    are categorical in the given dataframe and 
    returns them as lists
    '''

    numeric_columns = []
    categorical_columns = []
    for col in feat.columns:
        if feat[col].dtype in [int, float]:
            if feat[col].unique().shape[0] / feat.shape[0] < 0.01:
                categorical_columns.append(col)
            else:
                numeric_columns.append(col)
        else:
            categorical_columns.append(col)

    return numeric_columns, categorical_columns


def generate_single_column_plots(feat, label=None):
    '''
    returns a list of dcc.Graph objects

    feat must be pandas DataFrame object
    label must be pandas Series object
    '''
    numeric_columns, categorical_columns = _get_numeric_categorical_columns(
        feat)

    plots = []
    for col in numeric_columns:
        fig = _generate_histogram_plot_V2(feat=feat[col], label=label)
        graph_obj = dcc.Graph(figure=fig)
        plots.append(graph_obj)

    for col in categorical_columns:
        fig = _generate_freq_count_bar_plot(feat=feat[col], label=label)
        graph_obj = dcc.Graph(figure=fig)
        plots.append(graph_obj)

    return plots


def generate_multi_column_plots(feat, label=None):
    '''
    returns a list of dcc.Graph objects

    feat must be pandas DataFrame object
    label must be pandas Series object
    '''
    pass


def _generate_histogram_plot(feat, label=None):
    '''
    feat and label must be pandas Series object (single column)
    '''
    if label is not None:
        data = []
        for target_class in label.unique():
            trace = go.Histogram(
                x=feat[label == target_class], name=str(target_class))
            data.append(trace)
    else:
        trace = go.Histogram(x=feat)
        data = [trace]

    layout = go.Layout(
        title=feat.name,
        hovermode='closest'
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def _generate_histogram_plot_V2(feat, label=None):
    '''
    feat and label must be pandas Series object (single column)
    '''
    df = pd.DataFrame()
    df[feat.name] = feat
    if label is not None:
        df[label.name] = label
        fig = px.histogram(df, x=feat.name, color=label.name,
                           marginal="box", opacity=0.8, title=feat.name)
    else:
        fig = px.histogram(df, x=feat.name, marginal="box",
                           opacity=0.8, title=feat.name)

    return fig


def _generate_dist_plot(feat, label=None):
    '''
    feat and label must be pandas Series object (single column)
    '''
    if label is not None:
        data = []
        names = []
        for target_class in label.unique():
            data.append(feat[label == target_class])
            names.append(str(target_class))
    else:
        data = [feat]

    fig = ff.create_distplot(data, names)
    fig.update_layout(title_text=feat.name)
    return fig


def _generate_freq_count_bar_plot(feat, label=None):
    '''
    feat and label must be pandas Series object (single column)
    '''
    if label is not None:
        data = []
        for target_class in label.unique():
            categories, frequencies = zip(
                *sorted(feat[label == target_class].value_counts().to_dict().items(),
                        key=lambda x: x[1],
                        reverse=True))

            trace = go.Bar(
                x=frequencies,
                y=categories,
                orientation='h',
                name=str(target_class)
            )
            data.append(trace)

    else:
        categories, frequencies = zip(
            *sorted(feat.value_counts().to_dict().items(),
                    key=lambda x: x[1],
                    reverse=True))
        trace = go.Bar(
            x=frequencies,
            y=categories,
            orientation='h'
        )
        data = [trace]

    layout = go.Layout(
        title=feat.name,
        xaxis=dict(title='freq'),
        yaxis=dict(title=feat.name),
        hovermode='closest'
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def _generate_scatter_plot(x, y, label=None):
    '''
    x, y and label must be pandas Series object (single column)
    '''
    if label is not None:
        trace = go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                size=10,
                line=dict(width=1),
                color=label.astype('category').cat.codes
            )
        )

    else:
        trace = go.Scatter(
            x=x,
            y=y,
            mode='markers',
            marker=dict(
                size=10,
                line=dict(width=1)
            )
        )

    data = [trace]

    layout = go.Layout(
        title='{} VS {}'.format(x.name, y.name),
        xaxis=dict(title=x.name),
        yaxis=dict(title=y.name),
        hovermode='closest'
    )

    fig = go.Figure(data=data, layout=layout)
    return fig


def generate_corr_heatmap(feat, label=None):
    '''
    returns a correlation heatmap dcc.Graph object

    feat must be pandas DataFrame object
    label must be pandas Series object
    '''
    pass
