import pandas as pd
from util import funcs
from sources import ofac_sdn, us_bis

#%% static data
meta = {'columns':{'source':['Source','Source URL'],
                   'ofac_sdn':['Unique ID','SDN Name','SDN Type','Sanctions Programme'],
                   'us_bis':['Country','Name','Address']},

        'export_filename':'Sanctions Lists.xlsx'}

for i in [j for j in meta['columns'] if j not in ['source']]:
    meta['columns'][i] = meta['columns']['source'] + meta['columns'][i]

#%% initialise and pull raw data
dataframes = {}
dataframes[ofac_sdn.meta['list_name']] = ofac_sdn.clean_data(ofac_sdn.get_data(ofac_sdn.meta['url']))
dataframes[us_bis.meta['list_name']] = us_bis.clean_data(us_bis.get_data())

#%% create combined dataframe with selected columns
dataframes['Combined'] = dataframes[ofac_sdn.meta['list_name']][meta['columns']['ofac_sdn']].copy()
dataframes['Combined'].columns = [i.replace('SDN','Entity') for i in list(dataframes['Combined'])]

dataframes['Combined'] = pd.concat([dataframes['Combined'],
                                    dataframes[us_bis.meta['list_name']][meta['columns']['us_bis']].rename(columns={'Name':'Entity Name'})])

dataframes['Combined'].insert(len(meta['columns']['source']), 'Country', dataframes['Combined'].pop('Country'))

#%% export
funcs.save_xlsx(dataframes, meta['export_filename'], order=['Combined']+[i for i in list(dataframes) if i not in ['Combined']])