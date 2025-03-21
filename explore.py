"""
exploration of census tracts data
"""
import wget
import pandas as pd
from pygris import counties
import geopandas as gpd
from geodatasets import get_path
import contextily as cx
from matplotlib import pyplot as plt
import mpl_toolkits as mpl
import numpy as np


DATA_URL = 'https://raw.githubusercontent.com/aapeebles/iteam_exercise/refs/heads/main/data_files/Data%20exercise%20data%20-%20Sheet1.csv'
SHAPEFILE_PATH = 'data_files/muni_boundaries.zip'
PGH_TRACTS_FILE_PATH= "data_files/2020_census_hoods.csv"
ALLEGHENY_MUNI_TRACTS = "data_files/Allegheny_County_Municipalities_Census_Tracts_2000-2020.csv"

file_Path = 'data_files/census_data.csv'
shapefile_name = 'data_files/cb_2015_42_tract_500k.zip'
wget.download(SHAPEFILE_PATH, shapefile_name)
print('downloaded')

wget.download(DATA_URL, file_Path)
print('downloaded')

## importing and cleaning population data
vulnerable = pd.read_csv(DATA_URL, dtype = {"FIPS Code":"object"})
allegheny_pop = vulnerable.loc[(vulnerable.State.str.contains('Pennsylvania')) & (vulnerable.County.str.contains('Allegheny County')),:]
# get tract number
allegheny_pop['census_tract'] =  [x.split(';') for x in allegheny_pop['Location']]
allegheny_pop['census_tract_val'] = allegheny_pop.census_tract.apply(lambda x: x[0].split(' ')[-1] if x is not None else np.nan)
allegheny_pop['census_tract_val'].isna().sum()
# convert % overcrowded housing back to # for aggregation
allegheny_pop['overcrowded_count'] = allegheny_pop['Households']*(allegheny_pop['Percent of Overcrowded Housing Units']/100)


## import shapefile for allegheny county muni
allegheny_shapes = gpd.read_file(SHAPEFILE_PATH)
allegheny_shapes = allegheny_shapes.to_crs(epsg = 32617)
print(allegheny_shapes.head(2))
print('Shape: ', allegheny_shapes.shape)
print("\nThe shapefile projection is: {}".format(allegheny_shapes.crs))

### Get tracts that are within pittsburgh
aggregate_key = pd.read_csv('data_files/2020_census_hoods.csv', names=['neighborhood', 'year','tract'])
aggregate_key.drop(columns=['year'], inplace=True)
aggregate_key['reformat'] = [x.strip('()').split(',') for x in aggregate_key['tract']]
aggregate_key_full = aggregate_key.explode(['reformat']).reset_index(drop=True)
aggregate_key_full.drop(columns=['tract'], inplace=True)
aggregate_key_full.rename(columns={'reformat':'tract'},inplace=True)
pittsburgh_tracts = aggregate_key_full.loc[:,['tract']]
pittsburgh_tracts['municipality'] = 'Pittsburgh City'
pittsburgh_tracts.drop_duplicates(inplace=True)


## Get mapping of tracts to Allegheny County Municipalities
allegheny_munis_raw = pd.read_csv(ALLEGHENY_MUNI_TRACTS)
allegheny_munis = allegheny_munis_raw.iloc[:,[0,3]]
allegheny_munis.columns = ['municipality', 'tract']
allegheny_munis['tract'] = [x.strip('()').split(',') for x in allegheny_munis['tract']]
allegheny_munis = allegheny_munis.explode(['tract']).reset_index(drop=True)
allegheny_partial = allegheny_munis[~allegheny_munis['municipality'].isin(['Pittsburgh City', 'Osborne (Glen Osborne)' ])]
allegheny_partial.drop_duplicates(inplace=True)


allegheny_full = pd.concat([allegheny_partial, pittsburgh_tracts],axis=0)
# allegheny_full.head()
# allegheny_pop.head()
# allegheny_shapes.head()
allegheny_shapes.loc[allegheny_shapes.NAME.str.contains('GLENFIELD')]
# allegheny_partial.loc[allegheny_partial.municipality.str.contains('Sewickley')]


### Cleaning up mapping
allegheny_full.tract.unique().shape
tract_count = allegheny_full.groupby(by=['tract']).count()
updated_borough_names = allegheny_full.loc[allegheny_full['tract'].isin( tract_count.loc[tract_count['municipality']>1,:].index.to_list())].sort_values(by='tract').groupby('tract').agg(' & '.join).reset_index()
allegheny_full.loc[allegheny_full['tract'].isin( tract_count.loc[tract_count['municipality']>1,:].index.to_list())].sort_values(by='tract').municipality.str.upper()
borough_dict = dict(zip(updated_borough_names.tract.values, updated_borough_names.municipality.values))
borough_dict
updated_borough_names

allegheny.rename(columns={'FIPS Code':'GEOID'}, inplace=True)
pgh_tract.rename(columns={'geoid':'GEOID'}, inplace=True)
pgh_nbh.head()
allegheny.columns


pa_merge = pgh_tract.merge(allegheny, on='GEOID', how='inner')
pa_merge.columns

pa_merge['BIPOC % POP'] = pa_merge['BIPOC Residents'] /pa_merge['Population']
pa_merge['Overcrowded Households'] = pa_merge['Households']*(pa_merge['Percent of Overcrowded Housing Units']/100)
pa_merge[['Households','Overcrowded Households', 'Percent of Overcrowded Housing Units']].head()



fig, ax = plt.subplots(1, 1, figsize = (20, 10))


import matplotlib.pyplot as plt
from pygris import 



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