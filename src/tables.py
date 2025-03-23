""" 
producing summary and descriptive table that look nice
"""
import imgkit
import pandas as pd
pd.set_option('display.width', None)

READABLE_LABELS = ['% of Pop living at 150%\n of the poverty line',
                    '% of Pop who are BIPOC',
                    '% of Pop over 25 w/o \n high school diploma',
                    'Ratio of housholds to individuals',
                    '% of households w/o vehicle',
                    '% of households with overcrowding']

COLUMN_RANK_NAMES = ['rank_pov', 'rank_bipoc', 'rank_edu',
                     'rank_housing', 'rank_no_vehicle', 'rank_crowd']
agg_data = pd.read_pickle('data_files/tract_data_agged.pkl')

# subset dataset and create readable column labels
target_columns = [x for x in agg_data.columns.to_list() if '_perc' in x]
new_lables = dict(zip(target_columns, READABLE_LABELS))
col_dict = dict(zip(target_columns, COLUMN_RANK_NAMES))

muni_data =  agg_data[target_columns]

## create df of municipalities ranked by each index variable
for x,y in col_dict.items():
    muni_data[y] = muni_data[x].rank(ascending=False).astype('int')

base_df = pd.DataFrame(index=range(10))
for x,y in col_dict.items():
    temp = muni_data.loc[muni_data[y]<=10, [y,x]].sort_values(by=y).reset_index()\
        .drop(columns=[y]).copy()
    temp[f'{x}_muni'] = temp['municipality']+" : "+temp[x].map('{:.2%}'.format)
    base_df = pd.concat([base_df,temp[f'{x}_muni']], ignore_index=False, axis=1).copy()

base_df.index.name = 'rank'
base_df.set_index(base_df.index+1,inplace=True)
updated_col_names = dict(zip(base_df.columns.to_list(), READABLE_LABELS))
base_df.rename(columns=updated_col_names, inplace=True)
base_df = base_df.apply(lambda x: x.str.title())


# html1 = base_df.style.to_html()
# imgkit.from_string(html1, 'base_table.png')
# html3 = build_table(base_df.reset_index(), color='grey_light',  width='auto' )
# imgkit.from_string(html3, 'update1.png')

### Create img version of ranking table
styler = base_df.reset_index().style.set_table_styles([{'selector': 'table',
                                                        'props': [('width','1600px'),
                                                                  ('white-space','nowrap'),
                                                                   ('padding', '10px') ]},
                                                       {'selector': 'th',
                                                        'props': [('text-align', 'left'),
                                                                  ('white-space','nowrap'),
                                                                  ('padding', '10px')]}])\
                                                        .set_properties(**{'white-space': 'nowrap',
                                                                            'text-align': 'left',
                                                                            'padding': '0 20px'}).hide(axis="index")
html_string = styler.to_html()
imgkit.from_string(html_string, 'img/muni_ranking.png')


### Data Table summarizing statistics
percent_data =  agg_data[target_columns]
percent_data.rename(columns=new_lables, inplace=True)
percent_tidy = percent_data.describe()
styler2 = percent_tidy[percent_tidy.index!= 'count']\
    .style.format('{:.2%}').set_table_styles([{'selector': 'table',
                                               'props': [('width','1600px'),
                                                        ('white-space','nowrap'),
                                                        ('padding', '10px') ]},
                                             {'selector': 'th', 
                                                'props': [('text-align', 'left'),
                                                            ('white-space','nowrap'),
                                                            ('padding', '10px')]}])\
                                                            .set_properties(
                                                                **{'white-space': 'nowrap',
                                                                    'text-align': 'left',
                                                                    'padding': '0 20px'})

html_string2 = styler2.to_html()
imgkit.from_string(html_string2, 'img/allegheny_desc.png')
