import pandas as pd
import numpy as np
import logging
import base64
import io

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Process the data and make necessary changes before Plotting.
    Mostly Downsizing for better plot performance.

        Parameters: 
            df (DataFrame): A Pandas DataFrame

        Returns: 
            (DataFrame):    Post-Processed DataFrame
    '''

    # Casting the datatype to reduce the size of the file without
    # losing much information
    for column in df:
        if df[column].dtype == 'int64':
            df[column] = df[column].astype('int32')
        if df[column].dtype == 'float64':
            df[column] = df[column].astype('float16')
    
    # sampling
    #df = df.iloc[::17, :]
    
    ' Averaging every nth element '
    n = 20
    df = df.groupby(np.arange(len(df))//n).mean()

    return df


def parse_data(content, filename) -> pd.DataFrame:
    '''
    Read the csv file with the provided path

        Parameters:
            content ():     content of the data file
            filename (str): name of the data file

        Returns:
            (DataFrame):    Post-Processed DataFrame, whatever `format_data(...)` returns
    '''

    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    df=pd.DataFrame({'Time':[0]})
    print(filename)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))

    except Exception as e:
        logging.exception(e)

    return format_data(df)