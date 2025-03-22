"""
aggregate tract data up to county municipality levels
"""

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



pre_agg = pd.read_pickle('data_files/track_data_pre_agg.pkl')
pre_agg['overcrowded_count'] = pre_agg['overcrowded_count'].astype('int')
target_columns = pre_agg.select_dtypes(include='int').columns.to_list()
target_columns.append('municipality')
target_columns
agg_vul_factors = pre_agg[target_columns].groupby('municipality').agg('sum')

individual_level = ['Population','Ppl Below 150% Poverty', 'BIPOC Residents','People 25+ w/o high school diploma']
household_level = ['Households',  'Housing Units', 'Households with no vehicle', 'overcrowded_count',]

for var in individual_level[1:]:
    agg_vul_factors[f'{var}_perc'] = np.divide(agg_vul_factors[var],
                                               agg_vul_factors[individual_level[0]])

for var in household_level[1:]:
    agg_vul_factors[f'{var}_perc'] = np.divide(agg_vul_factors[var],
                                               agg_vul_factors[household_level[0]])

target_columns = [x for x in agg_vul_factors.columns.to_list() if '_perc' in x]
readable_labels = ['% of Pop living at 150%\n of the poverty line',
                    '% of Pop who are BIPOC',
                    '% of Pop over 25 w/o \n high school diploma',
                    'Ratio of housholds to individuals',
                    '% of households w/o vehicle',
                    '% of households with overcrowding']

new_lables = dict(zip(target_columns, readable_labels))

corr_matrix = agg_vul_factors[target_columns].corr()
corr_matrix = corr_matrix.rename(columns=new_lables, index=new_lables)

sns.heatmap(corr_matrix, cmap="Oranges", annot=True)
plt.xticks(rotation=45, ha='right')

plt.suptitle('Matrix of correlation between social vulnerability\n indicators across municipalities of Allegheny County')
plt.tight_layout()
plt.show()


agg_vul_factors.overcrowded_count_perc.plot(kind='density')
plt.show()


def make_pretty(styler):
    styler.set_caption('Distribution of target indicators across Allegheny Counts\n numbers shown as percent of population or percent of households')
    styler.
    styler.format_index(lambda v: v.strftime("%A"))
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
    return styler
agg_vul_factors[target_columns].describe().style.format("{:.2%}")

