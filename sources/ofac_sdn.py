import os
import pandas as pd
import numpy as np

if __name__=='__main__' and __package__ is None:
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util import funcs

#%%
meta = {'list_name':'OFAC Sanctions List',
        'url':'https://www.treasury.gov/ofac/downloads/consolidated/cons_prim.csv',
        'export_filename':'OFAC SDN_List.xlsx',

        # https://ofac.treasury.gov/media/29976/download?inline
        'columns':['Unique ID','SDN Name','SDN Type','Sanctions Programme','Title',
                   'Vessel Call Sign','Vessel Type','Vessel Tonnage','Vessesl Gross Registered Tonnage','Vessel Flag','Vessel Owner',
                   'Remarks']}

#%%
def get_data(url):
    df = pd.read_csv(url, encoding='utf-8', header=None)
    df.columns = meta['columns']
    return(df)

#%%
def clean_data(df):
    c_df = df.copy()
    c_df = c_df[[i for i in list(c_df) if not any(x in i.lower() for x in ['vessel'])]] # don't need these cols

    # basic string cleanup
    c_df = c_df.dropna(thresh=len(list(c_df))-1)
    c_df = c_df.map(lambda x:x.strip() if type(x)!=float else x)
    c_df = c_df.replace('-0-', np.nan)

    # sanctions programme cleanup
    c_df['Sanctions Programme'] = c_df['Sanctions Programme'].str.replace(' - ','-')
    for i in ['[',']']:
        c_df['Sanctions Programme'] = c_df['Sanctions Programme'].str.replace(i, '', regex=False)
    c_df['Sanctions Programme'] = c_df['Sanctions Programme'].apply(lambda x:x.split())
    c_df = c_df.explode('Sanctions Programme')

    c_df = c_df.dropna(how='all', axis=1)
    c_df = funcs.insert_source(c_df, meta['list_name'], meta['url'])
    return(c_df)

#%%
if __name__=='__main__':
    dataframes = {'Raw':get_data(meta['url'])}
    dataframes['Clean'] = clean_data(dataframes['Raw'])
    funcs.save_xlsx(dataframes, meta['export_filename'])