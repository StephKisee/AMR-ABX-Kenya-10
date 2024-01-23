import pandas as pd
import regex as re
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import seaborn as sns

palette = sns.color_palette('Spectral', 30)
def drop_repeated_prefix(df):
    for col in df.columns:
        if re.search(r'^\w\d+\.', col):
            print(col)
            df = df.drop(col, axis=1)
    return df


def create_geometry(df, coordinates_cols: list):
    """Create geometry column for geopandas dataframe."""
    df["geometry"] = df.apply(lambda x: Point(x[coordinates_cols[0]], x[coordinates_cols[1]]), axis=1)
    return df