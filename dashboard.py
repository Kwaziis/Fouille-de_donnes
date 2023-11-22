import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import engine

# Assuming you have a function get_forum_data() that returns a dictionary with forum data
# And a function get_top_forums() that returns a list of top 5 forums
forum_data = engine.dataProcessing("actions.json")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Table(id='top_index_table'),
    dcc.Slider(
        id='week-slider',
        min=0,
        max=len(forum_data['7']) - 1,  # assuming all forums have the same number of weeks
        value=len(forum_data['7']) - 1,
        marks={i: 'Week {}'.format(i) for i in range(len(forum_data['7']))},
        step=None
    ),
    dcc.Dropdown(
        id='forum-selector',
        options=[{'label': i, 'value': i} for i in forum_data.keys()],
        value='7'
    ),
    dcc.Graph(id='forum-graph'),
    html.Table(id='top-forums-table')
])

@app.callback(
    Output('forum-graph', 'figure'),
    [Input('forum-selector', 'value')]
)
def update_output(value):
    popularite_indice = engine.extract_populaire_indice(forum_data,value)[1:]
    dicute_indice = engine.extract_discute_indice(forum_data,value)[1:]
    active_indice = engine.extract_actif_indice(forum_data,value)[1:]

    dicute_indice = np.array(dicute_indice)
    if(np.max(dicute_indice) != 0):
        dicute_indice /= np.max(dicute_indice)

    x_axis = list(range(len(popularite_indice)))[1:]

    figure = {
    'data': [
        go.Scatter(
            x=x_axis,
            y=popularite_indice,
            mode='lines+markers',
            name='Popularity Index'
        ),
        go.Scatter(
            x=x_axis,
            y=dicute_indice,
            mode='lines+markers',
            name='Discussion Index'
        ),
        go.Scatter(
            x=x_axis,
            y=active_indice,
            mode='lines+markers',
            name='Activity Index'
        )
    ],
    'layout': go.Layout(
        title='Indicators of forum ' + value,
    )
    }

    return figure

@app.callback(
    Output('top_index_table', 'children'),
    [Input('week-slider', 'value')]
)
def update_tables(week):
    top_active_forums = engine.top_5_active_forums(forum_data, week)
    top_discussion_forums = engine.top_5_discussion_forums(forum_data, week)
    top_popular_forums = engine.top_5_popular_forums(forum_data, week)

    table = html.Table([
        html.Thead(
            html.Tr([html.Th('Forum'), html.Th('Top Active'), html.Th('Top Discussion'), html.Th('Top Popular')])
        ),
        html.Tbody([
            html.Tr([
                html.Td(i+1),
                html.Td(top_active_forums[i] if i < len(top_active_forums) else ''),
                html.Td(top_discussion_forums[i] if i < len(top_discussion_forums) else ''),
                html.Td(top_popular_forums[i] if i < len(top_popular_forums) else '')
            ]) for i in range(max(len(top_active_forums), len(top_discussion_forums), len(top_popular_forums)))
        ])
    ])

    return table
    

if __name__ == '__main__':
    app.run_server(debug=True)