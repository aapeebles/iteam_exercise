""" 
producing summary and descriptive table that look nice
"""

import pandas as pd
import imgkit

READABLE_LABELS = ['% of Pop living at 150%\n of the poverty line',
                    '% of Pop who are BIPOC',
                    '% of Pop over 25 w/o \n high school diploma',
                    'Ratio of housholds to individuals',
                    '% of households w/o vehicle',
                    '% of households with overcrowding']

column_rank_names = ['rank_pov', 'rank_bipoc', 'rank_edu', 'rank_housing', 'rank_no_vehicle', 'rank_crowd']

agg_data = pd.read_pickle('data_files/tract_data_agged.pkl')

# subset dataset and create readable column labels
target_columns = [x for x in agg_data.columns.to_list() if '_perc' in x]
new_lables = dict(zip(target_columns, READABLE_LABELS))

muni_data =  agg_data[target_columns]
col_dict = dict(zip(target_columns, column_rank_names))

for x,y in col_dict.items():
    muni_data[y] = muni_data[x].rank(ascending=False).astype('int')

base_df = pd.DataFrame(index=range(10))
for x,y in col_dict.items():
    temp = muni_data.loc[muni_data[y]<=10, [y,x]].sort_values(by=y).reset_index().drop(columns=[y]).copy()
    temp[f'{x}_muni'] = temp['municipality']+" : "+temp[y].map('{:.2%}'.format)
    base_df = pd.concat([base_df,temp[f'{x}_muni']], ignore_index=False).copy()
print(base_df)

