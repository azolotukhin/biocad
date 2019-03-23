import pandas as pd


def read_file(filename):
    df = pd.read_csv(filename, sep='\t', encoding='utf-8')
    print(df.shape)
    return df


def fix_date_format(dt):
    """fix dates from 2019-3-22 to 2019-03-22"""
    y, m, d = dt.split('-')
    m = ('0' + m)[-2:]
    d = ('0' + d)[-2:]
    return '-'.join((y, m, d))
