import geopandas as gpd
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import regex as re
import seaborn as sns

font_files = fm.findSystemFonts(fontpaths=None, fontext='otf')

for font_file in font_files:
    fm.fontManager.addfont(font_file)

font_size = 11
font_family = 'Gotham'
# plot_style = 'fivethirtyeight'
plot_style = 'seaborn-v0_8-paper'
plt.style.use(plot_style)
plt.rcParams['grid.alpha'] = 0.5
plt.rcParams['font.size'] = font_size
plt.rcParams['font.family'] = font_family
plt.rcParams['axes.labelsize'] = font_size
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = font_size
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.titlelocation'] = 'left'
plt.rcParams['xtick.labelsize'] = font_size
plt.rcParams['ytick.labelsize'] = font_size
plt.rcParams['legend.fontsize'] = font_size
plt.rcParams['figure.titlesize'] = font_size
plt.rcParams['figure.titleweight'] = 'bold'
# plt.rcParams['figure.titlelocation'] = 'left'
plt.rcParams['figure.constrained_layout.use'] = True
# plt.rcParams['figure.constraint_layout.use'] = True


palette = sns.color_palette('Spectral')


def get_prefixes(df: pd.DataFrame) -> tuple:
    prefixes = [col.split(' ', 1)[0] + ' ' for col in df.columns if col.count('/') > 0]
    prefix_counts = {prefix: prefixes.count(prefix) for prefix in prefixes}
    prefixes = [prefix for prefix in prefixes if prefix_counts[prefix] > 1]
    n_prefixes = len(prefixes)
    unique_prefixes = list(set(prefixes))
    n_unique_prefixes = len(unique_prefixes)

    return prefixes, unique_prefixes, n_prefixes, n_unique_prefixes


def assign_cols(df: pd.DataFrame, prefixes: list) -> tuple:
    initial_cols = []

    for prefix in prefixes:
        for col in df.columns:
            if col.startswith(prefix):
                initial_cols.append(col)
                break

    encoded_cols = []

    for col in df.columns:
        for prefix in prefixes:
            if col.startswith(prefix):
                encoded_cols.append(col)

    encoded_cols = [col for col in encoded_cols if col not in initial_cols]

    return initial_cols, encoded_cols


def create_col_dict(initial_cols: list, encoded_cols: list) -> dict:
    col_dict = {}

    for col in encoded_cols:
        prefix = col.split(' ', 1)[0] + ' '
        for col_ in initial_cols:
            if col_.startswith(prefix):
                col_dict[col] = col_
                break

    return col_dict


def create_values_replace_map(col_dict: dict) -> dict:
    val_dict = {}

    for k, v in col_dict.items():
        val_dict[k] = k.replace(v, '')

    for k, v in val_dict.items():
        if v.startswith('/'):
            val_dict[k] = v[1:]

    return val_dict


def create_names_replace_map(initial_cols: list, unique_prefixes: list) -> dict:
    names_dict = {}

    old = [prefix + 'value' for prefix in unique_prefixes]

    for i in old:
        for col in initial_cols:
            if i.split(' ', 1)[0] in col:
                names_dict[i] = col
                break

    return names_dict


def melt_cols(df: pd.DataFrame, prefixes: list):
    if not isinstance(prefixes, list):
        prefixes = list(prefixes)

    for prefix in prefixes:
        cols = [col for col in df.columns if col.startswith(prefix)]
        df = df.melt(id_vars=[col for col in df.columns if col not in cols],
                     value_vars=cols,
                     var_name=prefix,
                     value_name=prefix + 'value')

    return df


# def melt_df(df: pd.DataFrame):