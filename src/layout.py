# Built-in Libraries.
import os

# Thir Party Libraries.
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

# local modules
from src.plot import plot_side_info, simple_plot, side_by_side_plots

def update_graphs(df: pd.DataFrame) -> list:
    '''
    Setup The Data Graphs After A File Has Been Uploaded And Parsed.
    Edit,Add and/or Remove Graphs Here Following the General Format.

        Parameters:
            df (DataFrame): DataFrame After Parsing and Formatting.

        Returns:
            (list): List Of HTML ELements As The Children Of The Main Div.
    '''
    return [
        # Spacing at top of the page
        html.Div(style={'marginTop':'100px'}),

        # Plot 1
        plot_side_info(
            df[['Time','TC_FU_LINE_1','TC_FU_LINE_2','TC_FU_TANK'
                ,'TC_OX_LINE_1','TC_OX_LINE_2','TC_OX_TANK']],
            title='SFS Temperature'
        ),
        html.Br(),

        # Plot2            
        side_by_side_plots(
            df_left=df[['Time','ACT_FU_MAIN','ACT_FU_PRESS','ACT_FU_VENT',
                'ACT_FU_PURGE','ACT_MBV']], 
            df_right=df[['Time','ACT_OX_MAIN','ACT_OX_PRESS','ACT_OX_VENT',
                'ACT_OX_PURGE','ACT_MBV']],
            title_left='FUEL Side Valves Actuation',
            title_right='LOX Side Valves Actuation',
        ),
        html.Br(),

        # Plot3            
        simple_plot(
            df[['Time','TC_ENG_7','TC_ENG_9','TC_ENG_10','TC_ENG_11'
                ,'TC_ENG_17','TC_ENG_18','TC_ENG_20','TC_ENG_21']],
            title='Engine Temperatures'
        ),
        html.Br(),
    ]

def setup_layout(app: Dash) -> html.Div:
    '''
    Setup the layout used to initialized the Dash App.
    Structure is similar to HTML format.

        Parameters:
            app (Dash):     

        Returns:
            (html.Div):     A Div element from the Dash.html
    '''

    return html.Div(children=[html.Div(
        id='main-div',
        children=[
            html.Div('No Data', style={
                'marginTop':'400px',
                'textAlign':'center',
                'fontSize':'35pt',
                'color':'rgba(255,255,255,0.3)'
            })
        ], style={'padding':'20px 40px'}

        # NavBar    
        ),
        html.Div(
            children=setup_NavBar('TEMP FILE NAME'), 
            className='navBar', id='nav-bar'
        )
    ])


def setup_NavBar(filename: str) -> list :
    '''
    Does its thing

        Parameters:  
            filename (str): Name of the csv data file

        Returns:
            (list):         List Of HTML ELements As Children
    '''

    # Layout Of The Website
    return [
        dbc.Row([
            dbc.Col(html.Img(src='assets/images/Logo_Color.svg', className='logo'), width = 'auto'),
            dbc.Col(html.Div(children=[
                html.Div(children=[
                    html.Span(filename,style={'--index':0}),
                    html.Span(filename,style={'--index':1}),
                    html.Span(filename,style={'--index':2}),
                ],className='header',style={'--element-count':3})        
            ]),width = 'auto')
        ],className=['g-0'], justify='start',align='bottom'),
        dcc.Upload(
            id = 'file-selector',
            children=[html.Div('Upload')]
        ),
    ]