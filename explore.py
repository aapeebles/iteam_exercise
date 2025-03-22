"""
exploration of census tracts data
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pygris import 



pa_merge = pgh_tract.merge(allegheny, on='GEOID', how='inner')
pa_merge.columns

pa_merge['BIPOC % POP'] = pa_merge['BIPOC Residents'] /pa_merge['Population']
pa_merge['Overcrowded Households'] = pa_merge['Households']*(pa_merge['Percent of Overcrowded Housing Units']/100)
pa_merge[['Households','Overcrowded Households', 'Percent of Overcrowded Housing Units']].head()



fig, ax = plt.subplots(1, 1, figsize = (20, 10))






#http://server.arcgisonline.com/arcgis/rest/services
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

plt.show()

# Plot data
# Source: https://geopandas.readthedocs.io/en/latest/docs/user_guide/mapping.html




pgh_nbh.plot(figsize=(10, 10),
                       cmap = "RdPu")
pgh_nbh.boundary.plot()
plt.show()


pgh_nbh.columns
pgh_nbh
pa_merge.columns
pa_merge.rename(columns={'GEOID':'GEOID_BLOCK'}, inplace=True)
pgh_nbh.rename(columns = {}, inplace = True)

print(pgh_nbh[['neighbor_', 'neighbor_i', 'hood', 'hood_no', 'geometry', 'OBJECTID', 'fid_blockg', 'statefp10', 'countyfp10', 'tractce10',
       'blkgrpce10', 'geoid10', 'namelsad10', 'mtfcc10', 'funcstat10',
       'aland10',]].head())

print(pa_merge[['OBJECTID', 'statefp', 'countyfp', 'tractce', 'GEOID', 'name',
       'namelsad', 'mtfcc', 'funcstat', 'aland', 'awater', 'intptlat',
       'intptlon', 
       'Location',]].head())
update_pitt = pa_merge[['Population', 'Housing Units',
       'Households', 'Ppl Below 150% Poverty', 'BIPOC Residents',
       'Households with no vehicle', 'Overcrowded Households',
       'People 25+ w/o high school diploma', 'geometry', ]].to_crs(epsg = 32617)
update_nbr = pgh_nbh[['hood','geometry']].to_crs(epsg = 32617)

type(update_nbr)

test = update_nbr.sjoin( update_pitt, how='left',predicate= 'within')
update_nbr.shape
test.shape
test.head()
type(test)
ax = pa_merge.plot(column = "BIPOC Residents",
                       figsize=(10, 10),
                       cmap = "RdPu",
                       legend = True,
                       alpha=0.5)
cx.add_basemap(ax)
# Set title
ax.set_title('BIPOC percent by census tract in Pittsburgh', fontdict = {'fontsize': '25', 'fontweight' : '3'})

plt.show()

type(test)
from mpl_toolkits.basemap import Basemap

update_nbr.boundary.plot()
plt.show()


def get_relation(df, col1, col2):        
    first_max = df[[col1, col2]].groupby(col1).count().max()[0]
    second_max = df[[col1, col2]].groupby(col2).count().max()[0]
    if first_max==1:
        if second_max==1:
            return 'one-to-one'
        else:
            return 'one-to-many'
    else:
        if second_max==1:
            return 'many-to-one'
        else:
            return 'many-to-many'

from itertools import product
for col_i, col_j in product(df.columns, df.columns):
    if col_i == col_j:
        continue
    print(col_i, col_j, get_relation(df, col_i, col_j))

get_relation(pgh_nbh, 'fid_blockg', "hood_no")
pgh_nbh.columns
pgh_nbh.head()

pgh_nbh[['fid_blockg', "hood_no"]]


aggregate_key_full.columns 
aggregate_key_full.shape
pa_merge.shape
pd.merge(pa_merge,aggregate_key_full,on=['name'],how='left') 