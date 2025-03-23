"""
aggregate tract data up to county municipality levels
"""

import numpy as np
import pandas as pd

INDIVIDUAL_LEVEL = ['Population','Ppl Below 150% Poverty',
                    'BIPOC Residents','People 25+ w/o high school diploma']
HOUSEHOLD_LEVEL = ['Households',  'Housing Units',
                   'Households with no vehicle', 'overcrowded_count',]

def agg_tract_data(file_name):
    """ assumtpion: file name points to a pkl file"""

    pre_agg = pd.read_pickle(f'data_files/{file_name}')
    pre_agg['overcrowded_count'] = pre_agg['overcrowded_count'].astype('int')
    target_columns = pre_agg.select_dtypes(include='int').columns.to_list()
    target_columns.append('municipality')
    agg_vul_factors = pre_agg[target_columns].groupby('municipality').agg('sum')


    for var in INDIVIDUAL_LEVEL[1:]:
        agg_vul_factors[f'{var}_perc'] = np.divide(agg_vul_factors[var],
                                                agg_vul_factors[INDIVIDUAL_LEVEL[0]])

    for var in HOUSEHOLD_LEVEL[1:]:
        agg_vul_factors[f'{var}_perc'] = np.divide(agg_vul_factors[var],
                                                agg_vul_factors[HOUSEHOLD_LEVEL[0]])
    return agg_vul_factors

agg_vul_factors = agg_tract_data('track_data_pre_agg.pkl')
agg_vul_factors.to_pickle('data_files/tract_data_agged.pkl')
