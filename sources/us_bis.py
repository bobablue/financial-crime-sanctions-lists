import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

if __name__=='__main__' and __package__ is None:
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util import funcs

#%%
meta = {'list_name':'US BIS List',
        'url':'https://www.ecfr.gov/current/title-15/subtitle-B/chapter-VII/subchapter-C/part-744/appendix-Supplement%20No.%204%20to%20Part%20744',
        'headers':{'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0'},
        'export_filename':'US BIS_List.xlsx'}

#%%
def get_data():
    response = requests.get(url=meta['url'], headers=meta['headers'])
    bs_obj = BeautifulSoup(response.content, 'html.parser')

    headers = [' '.join(i.text.split()) for i in bs_obj.find('thead').find_all('th')]
    table = bs_obj.find('tbody')

    columns = 5
    rows = [i.text for i in table.find_all('td')]
    rows = np.reshape(rows, (int(len(rows)/columns), columns))

    df = pd.DataFrame(rows, columns=headers)
    return(df)

#%%
def clean_data(df):
    c_df = df.copy()

    for i in ['', ' ','\n']:
        c_df = c_df.replace(i, np.nan)

    c_df['Country'] = c_df['Country'].ffill()

    # split entity name out
    c_df['Entity Split_1'] = c_df['Entity'].str.split(',', n=1).str[0]
    c_df['Entity Split_2'] = c_df['Entity'].str.split(',', n=1).str[-1]
    for i in [x for x in list(c_df) if x.startswith('Entity Split')]:
        c_df[i] = c_df[i].str.strip()
    c_df = c_df.drop(['Entity'], axis=1)

    c_df = c_df.rename(columns={'Entity Split_1':'Name', 'Entity Split_2':'Address'})
    c_df.insert(list(c_df).index('Country')+1, 'Name', c_df.pop('Name'))
    c_df.insert(list(c_df).index('Name')+1, 'Address', c_df.pop('Address'))

    c_df = funcs.insert_source(c_df, meta['list_name'], meta['url'])
    return(c_df)

#%%
if __name__=='__main__':
    dataframes = {'Raw':get_data()}
    dataframes['Clean'] = clean_data(dataframes['Raw'])
    funcs.save_xlsx(dataframes, meta['export_filename'])