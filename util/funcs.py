import pandas as pd

#%%
def insert_source(df, name, url):
    s_df = df.copy()
    s_df.insert(0, 'Source URL', url)
    s_df.insert(0, 'Source', name)
    return(s_df)

#%%
def save_xlsx(list_dfs, filepath, order=None):
    if not order:
        order = list(list_dfs)
    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        for ws in order:
            index = list_dfs[ws].index.nlevels if list_dfs[ws].index.nlevels>1 else 0
            panes = (list_dfs[ws].columns.nlevels, index)

            list_dfs[ws].to_excel(writer, sheet_name=ws, freeze_panes=panes, index=False)

            writer.sheets[ws].autofilter(*[list_dfs[ws].columns.nlevels-1,
                                           0,
                                           list_dfs[ws].columns.nlevels-1,
                                           index+len(list_dfs[ws].columns)-1])