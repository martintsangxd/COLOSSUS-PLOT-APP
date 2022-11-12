__author__ = "Martin Zeng"
__status__ = "Developing"

### Step 1
# need to install a few FrameWorks to use it
# `pip install dash`
# `pip install pandas`
# `pip install dash-bootstrap-components`
# `pip install plotly`
# `pip install numpy`
# And Any Other FrameWork That It Requires

### Step 2
# Run this app with `python app.py` and

### Step 3
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, State, ctx
from dash_bootstrap_components import themes
import webbrowser
import pandas as pd
from threading import Timer
from src.layout import setup_layout
from tkinter import filedialog

# local modules
from src.read_data import parse_data
from src.layout import update_graphs, setup_NavBar

app = Dash(__name__, external_stylesheets=[themes.BOOTSTRAP])


# Updates The Graphs/ Layout Of The Main Div
# After The User Has Uploaded A Data File.
@app.callback(
    Output('main-div', 'children'),
    Output('nav-bar', 'children'),
    Input('file-selector', 'contents'),
    State('file-selector', 'filename'))
def update_output(content,filename):
    if content is not None:
        df = parse_data(content, filename)
        return update_graphs(df), setup_NavBar(filename.split('.')[0])

    return html.Div('No Data', style={
                'marginTop':'400px',
                'textAlign':'center',
                'fontSize':'35pt',
                'color':'rgba(255,255,255,0.3)'
    }), setup_NavBar('TEMP FILE NAME')


def open_browser():
    webbrowser.open_new("http://localhost:{}".format(8050))


def main() -> None:
    # Using dash bootstrap components
    app.title = 'CURVE 2.0'
    app.layout = setup_layout(app)

    #Timer(1, open_browser).start()
    app.run_server(debug=True)
    
if __name__ == '__main__':
    main()