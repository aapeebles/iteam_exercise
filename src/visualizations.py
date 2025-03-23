import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter 
from mpl_toolkits.axes_grid1 import make_axes_locatable
import geopandas as gpd


READABLE_LABELS = ['% of Pop living at 150%\n of the poverty line',
                    '% of Pop who are BIPOC',
                    '% of Pop over 25 w/o \n high school diploma',
                    'Ratio of housholds to individuals',
                    '% of households w/o vehicle',
                    '% of households with overcrowding']

# import data
agg_data = pd.read_pickle('data_files/tract_data_agged.pkl')

# subset dataset and create readable column labels
target_columns = [x for x in agg_data.columns.to_list() if '_perc' in x]
new_lables = dict(zip(target_columns, READABLE_LABELS))


#### Correlation Heat Map
corr_matrix = agg_data[target_columns].corr()
corr_matrix = corr_matrix.rename(columns=new_lables, index=new_lables)
sns.heatmap(corr_matrix, cmap="Oranges", annot=True)
plt.xticks(rotation=45, ha='right')
plt.suptitle('Matrix of correlation between social vulnerability\n indicators across municipalities of Allegheny County')
plt.tight_layout()
plt.savefig('img/corr_matrix.png')
plt.show()


### BOXPLOT
"""
get specified columns. Omitted housing unit ratio because it is at such
a larger scale than the others
"""
subset_dict = {j:k for j,k in new_lables.items() if j!='Housing Units_perc' }
subset_list = [j for j in target_columns if j!='Housing Units_perc' ]
fig, ax = plt.subplots()
ax.boxplot(agg_data[target_columns], orientation='horizontal', )
ax.set_yticks(range(1, len(subset_dict.values()) +1))
ax.set_yticklabels(subset_dict.values())
ax.xaxis.set_major_formatter(PercentFormatter(1)) 
plt.suptitle('Distribution of conditions across Allegheny County Municipalities')
plt.tight_layout()
plt.grid()
plt.savefig('img/boxplot_dist.png')
plt.show()


### MAPPING

agg_data.reset_index(inplace=True)
agg_data.columns
county_data = pd.read_pickle('data_files/county_shapes_cleaned.pkl')



# Create the GeoDataFrame
county_shapes = gpd.GeoDataFrame(county_data, geometry= county_data['geometry'], crs="EPSG:32617")
county_shapes.boundary.plot()
plt.show()

target_df = pd.merge( county_shapes[['NAME_TRACT', 'geometry']] ,
                     agg_data[['municipality','Ppl Below 150% Poverty_perc']],
                     left_on='NAME_TRACT',
                     right_on='municipality')

target_df['rank'] = target_df['Ppl Below 150% Poverty_perc'].rank(ascending=False).astype('int')
table = target_df[target_df['rank']<=10].loc[:,['rank','NAME_TRACT']].sort_values(by='rank')
table['NAME_TRACT'] = table['NAME_TRACT'].str.capitalize()
table.rename(columns={'NAME_TRACT':'Municipality'}, inplace = True)

### MAP IT
fig, ax = plt.subplots(figsize=(12, 8))
divider = make_axes_locatable(ax)
cax = divider.append_axes("bottom", size="5%", pad=0.1)
target_df.plot( column='Ppl Below 150% Poverty_perc', cmap='OrRd',
                       alpha=0.5,
                       ax=ax,
                       cax=cax,
                       legend =True,
                       legend_kwds={"label": "Percentage of Population in each Muncuipality\n Living beneath 150% of the poverty level", "orientation": "horizontal"},)
target_df.boundary.plot(ax=ax, color='grey')

target_df[target_df['rank']<=10].apply(lambda x: ax.annotate(text= x['rank'], xy=x.geometry.centroid.coords[0], ha='center', weight='bold'), axis=1)
table_box = ax.table(cellText=table.values,
                     colLabels=table.columns,
                  loc='lower left',
                  cellLoc='left')
                  # bbox adjusts table position and size
table_box.auto_set_column_width(col=list(range(len(table.columns))))
ax.set_title('Analyzing the Distribution of Poverty\nacross Allegheny County')
# Adjust layout to prevent overlap
plt.tight_layout()
plt.savefig('img/poverty_map.png')
plt.show()




def make_pretty(styler):
    styler.set_caption('Distribution of target indicators across Allegheny Counts\n numbers shown as percent of population or percent of households')
    styler.
    styler.format_index(lambda v: v.strftime("%A"))
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGnBu")
    return styler
descriptive_stats = agg_data[target_columns].describe()
plt.tight_layout()
print(descriptive_stats.rename(columns=new_lables).iloc[1:].map('{:.2%}'.format))
# print(descriptive_stats.map('{:.2%}'.format))




