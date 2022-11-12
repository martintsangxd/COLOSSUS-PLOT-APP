# Third Party Libraries
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Builit-in
import logging

# Local Modules
from src.Constants import fill_colors, line_colors, styling_text

sample_df = pd.DataFrame({'Time':[0]})

figures = []

def _update_layout(fig: go.Figure):
    '''
    Golbal Styling For All The Figure That Is Processed By Plotly

        Parameters:
            fig (Figure): A Figure instance from the graph_objects Library
    '''
    custom_legend = go.layout.Legend(bgcolor='rgba(0,0,0,0)', orientation='h')
    custom_template = dict(
        layout = go.Layout(legend = custom_legend, font=dict(family='Orbitron, Nasalization, Arial', color='white',size=10),
        margin=dict(t=25, b=30,r=25)
    ))

    fig.update_layout(
        paper_bgcolor='rgb(39,34,39)', plot_bgcolor='rgba(0,0,0,0)',
        legend_title='',
        height=450,
        modebar=dict(bgcolor='rgba(0,0,0,0)'), 
        template=custom_template,
        hovermode='x unified', hoverdistance=25,
        hoverlabel=dict(
            bgcolor='rgba(32,11,11,0.5)',
            bordercolor='rgba(32,11,11,0.5)',
        ),
    )


def _create_line_chart(df: pd.DataFrame=None) -> go.Figure:
    '''
    Does What Its Name Suggests. 
    Used the DataFrame Provided To Render A Plot Figure From Plotly

        Parameters:
            df (DataFrame): The DataFrame Containing a Time Column with other SNSR Columns
        Returns:
            (Figure):       A Plotly Line Chart Figure (Scatter)
    '''
    
    fig = go.Figure()

    ind = 0
    for column in df:
        if column != 'Time':
            fig.add_trace(go.Scatter(
                x=df['Time'], y=df[column], name=column, 
                line=dict(width=1, color=line_colors[ind%(len(line_colors)+1)]),
                fill='tozeroy',
                fillcolor=fill_colors[ind%(len(fill_colors)+1)]
            ))
            ind += 1

    # More styling
    fig.update_traces(hovertemplate=None)
    _update_layout(fig)
    fig.update_xaxes(gridcolor='rgba(255,255,255,0.15)', tickprefix='T+', showline=True)
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.15)', ticksuffix=' unit ', title='',fixedrange=True)
    return fig


def simple_plot(df: pd.DataFrame, title: str='TITLE') -> html.Div:
    '''
    Uses The `_create_line_chart(...)` Function To Create A Div
    That Spans the Entire Window.

        Parameters:
            df (DataFrame): The DataFrame Containing a Time Column with other SNSR Columns
            title (str):    Title & Name For The Plot.
        Returns:
            (Div):          A Div Element Containing The Plot Figure.
    '''
    if not validity_check(df):
        df = sample_df
    return html.Div(dbc.Row([
        dbc.Col(html.Div([
            html.Div(title, className='plot-title'),
            html.Div(styling_text, className='plot-tag'),
            dcc.Graph(id=title, figure=_create_line_chart(df))
        ],className='plot'), width=12)
    ]))


def side_by_side_plots(df_left:pd.DataFrame, df_right:pd.DataFrame, title_left:str='TITLE1', title_right: str='TITLE2') -> html.Div:
    '''
    Uses The `_create_line_chart(...)` Function To Create A Div Containing
    Two Side-By-Side Plot DiviDing the Window In Half.

        Parameters:
            df_left (DataFrame):    The DataFrame For The Figure On The Left
            df_right (DataFrame):   The DataFrame For The Figure On The Right
        Returns:
            (Div):                  A Div With Two Plotly Figures
    '''

    #if not validity_check(df_left):
    #    df_left = sample_df
    #if not validity_check(df_right):
    #    df_right = sample_df

    return html.Div(dbc.Row([
        dbc.Col(html.Div([
            html.Div(title_left, className='plot-title'),
            html.Div(styling_text, className='plot-tag'),
            dcc.Graph(id=title_left, figure=_create_line_chart(df_left))
        ],className='plot'), width=6),
        dbc.Col(html.Div([
            html.Div(title_right, className='plot-title'),
            html.Div(styling_text, className='plot-tag'),
            dcc.Graph(id=title_right, figure=_create_line_chart(df_right))
        ],className='plot'), width=6),
    ]))


def plot_side_info(df: pd.DataFrame, title: str='TITLE') -> html.Div:
    '''
    Creates a Div Containing A Plotly Figure On The Left Side,
    And A Additional Table With Min Max Values Display alongside
    With A BoxPlot As Side Infos.

        Parameters:
            df_left (DataFrame):    The DataFrame For The Figure On The Left
            df_right (DataFrame):   The DataFrame For The Figure On The Right
        Returns:
            (Div):                  A Div With Two Plotly Figures
    '''

    #if not validity_check(df):
    #    df = sample_df

    table_header = [
        html.Thead(html.Tr([html.Th('SNSR'),html.Th('Min'),html.Th('Max')]))
    ]

    rows = []
    for snsr in df:
        if snsr != 'Time':
            rows.append(html.Tr([html.Td(snsr),html.Td(df[snsr].min()),html.Td(df[snsr].max())]))
    table_body = [html.Tbody(rows)]
    table = html.Table(table_header + table_body)

    return html.Div(dbc.Row([
        dbc.Col(html.Div([
            html.Div(title, className='plot-title'),
            html.Div(styling_text, className='plot-tag'),
            dcc.Graph(id=title, figure=_create_line_chart(df))
        ],className='plot'), width=9),
        dbc.Col(
            html.Div(children=[
                html.Div([table, html.Div(id='bottom-view')], className='table-view'),
                dcc.Graph(
                    figure=create_boxplot(df), 
                    config={'displayModeBar': False}
                )
            ], 
            className='info-view'),
            style={'paddingRight':'10px'}, width = 3
        ),
    ]))


def create_boxplot(df: pd.DataFrame) -> go.Figure:
    '''
    Creates a Div Containing A Plotly Figure On The Left Side,
    And A Additional Table With Min Max Values Display alongside
    With A BoxPlot As Side Infos.

        Parameters:
            df_left (DataFrame):    The DataFrame For The BoxPlot
        Returns:
            (Figure):               A Plotly BoxPlot Figure
    '''

    #if not validity_check(df):
    #    df = sample_df

    custom_legend = go.layout.Legend(bgcolor='rgba(0,0,0,0)',y=0.99)
    custom_template = dict(
        layout = go.Layout(legend = custom_legend, font=dict(family='Orbitron, Nasalization, Arial', color='white',size=10),
        margin=dict(t=75, b=75,l=0,r=0))
    )

    fig = go.Figure()
    count = 0
    show = True
    for snsr in df:
        if snsr != 'Time':
            if count > 0:
                show = False
            fig.add_trace(go.Box(x=df[snsr],name=snsr, boxmean=True, notched=True,marker_color='rgb(255,255,255)',visible=show))
            count+=1
                
    fig.update_xaxes(showline=False,showgrid=True,gridcolor='rgba(255,255,255,0.05)')
    fig.update_yaxes(showline=False,showgrid=False, showticklabels=False)
    fig.update_layout(
        title='',
        paper_bgcolor='rgb(39,34,39)', plot_bgcolor='rgba(0,0,0,0)',
        template=custom_template, height=200, hovermode='x unified'
    )
    return fig


def validity_check(df: pd.DataFrame) -> bool:
    '''
    Checks If The Dataframe Passed In Is Of the Correct Format.

        Parameters:
            df_left (DataFrame):    The DataFrame To Be Checked
        Returns:
            (bool):                 True Indicating Check Passed, False Otherwise
    '''
    
    if len(df.columns) < 2:
        logging.exception('Not Enough Data Columns')
        return False
    if 'Time' not in df.columns:
        logging.exception('No Time Info')
        return False
    return True