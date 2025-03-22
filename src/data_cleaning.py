"""
data cleaning work mapping tracts to municipalities within allegheny county
"""

import numpy as np
import wget
import pandas as pd
import geopandas as gpd

DATA_URL = 'https://raw.githubusercontent.com/aapeebles/iteam_exercise/refs/heads/main/data_files/Data%20exercise%20data%20-%20Sheet1.csv'
SHAPEFILE_PATH = 'data_files/muni_boundaries.zip'
PGH_TRACTS_FILE_PATH= "data_files/2020_census_hoods.csv"
ALLEGHENY_MUNI_TRACTS = "data_files/Allegheny_County_Municipalities_Census_Tracts_2000-2020.csv"

FILE_PATH = 'data_files/census_data.csv'
SHAPEFILE_NAME = 'data_files/cb_2015_42_tract_500k.zip'
wget.download(SHAPEFILE_PATH, SHAPEFILE_NAME)
print('downloaded')

wget.download(DATA_URL, FILE_PATH)
print('downloaded')

## importing and cleaning population data
vulnerable = pd.read_csv(DATA_URL, dtype = {"FIPS Code":"object"})
allegheny_pop = vulnerable.loc[(vulnerable.State.str.contains('Pennsylvania'))
                               & (vulnerable.County.str.contains('Allegheny County')),:]
# get tract number
allegheny_pop['census_tract'] =  [x.split(';') for x in allegheny_pop['Location']]
allegheny_pop['tract'] = (allegheny_pop.census_tract
                          .apply(lambda x: x[0].split(' ')[-1] if x is not None else np.nan))
allegheny_pop['tract'].isna().sum()
# convert % overcrowded housing back to # for aggregation
allegheny_pop['overcrowded_count'] = np.multiply( allegheny_pop['Households'],
                                                 (np.divide(allegheny_pop['Percent of Overcrowded Housing Units'],
                                                            100)))
## import shapefile for allegheny county muni
allegheny_shapes = gpd.read_file(SHAPEFILE_PATH)
allegheny_shapes = allegheny_shapes.to_crs(epsg = 32617)
print(allegheny_shapes.head(2))
print('Shape: ', allegheny_shapes.shape)
print(f"\nThe shapefile projection is: {allegheny_shapes.crs}")

### Get tracts that are within pittsburgh
aggregate_key = pd.read_csv('data_files/2020_census_hoods.csv',
                            names=['neighborhood', 'year','tract'])
aggregate_key.drop(columns=['year'], inplace=True)
aggregate_key['reformat'] = [x.strip('()').split(',') for x in aggregate_key['tract']]
aggregate_key_full = aggregate_key.explode(['reformat']).reset_index(drop=True)
aggregate_key_full.drop(columns=['tract'], inplace=True)
aggregate_key_full.rename(columns={'reformat':'tract'},inplace=True)
pittsburgh_tracts = aggregate_key_full.loc[:,['tract']]
pittsburgh_tracts['municipality'] = 'Pittsburgh'
pittsburgh_tracts.drop_duplicates(inplace=True)


## Get mapping of tracts to Allegheny County Municipalities
allegheny_munis_raw = pd.read_csv(ALLEGHENY_MUNI_TRACTS)
allegheny_munis = allegheny_munis_raw.iloc[:,[0,3]]
allegheny_munis.columns = ['municipality', 'tract']
allegheny_munis['tract'] = [x.strip('()').split(',') for x in allegheny_munis['tract']]
allegheny_munis = allegheny_munis.explode(['tract']).reset_index(drop=True)
removed_cities = ['Pittsburgh City', 'Osborne (Glen Osborne)' ]
allegheny_partial = allegheny_munis[~allegheny_munis['municipality'].isin(removed_cities)]
allegheny_partial.municipality.replace({'Glen Osborne (Osborne)':'Glen Osborne'}, inplace=True)
allegheny_partial.drop_duplicates(inplace=True)

PATTERN = '|'.join(allegheny_shapes.TYPE.value_counts().index.to_list())

allegheny_full = pd.concat([allegheny_partial, pittsburgh_tracts],axis=0)
allegheny_full['municipality'] = allegheny_full['municipality'].str.upper()
allegheny_full['municipality'] = allegheny_full['municipality'].str.replace(PATTERN, '', regex=True)
allegheny_full['municipality'] = allegheny_full['municipality'].str.strip()
allegheny_full.head()

### Cleaning up mapping
tract_count = allegheny_full.groupby(by=['tract']).count()
updated_borough_names = (allegheny_full.loc[allegheny_full['tract']
                                            .isin( tract_count.loc[tract_count['municipality']>1,:]
                                                  .index.to_list())]
                                                  .sort_values(by='tract')
                                                  .groupby('tract')
                                                  .agg(' & '.join)
                                                  .reset_index())

original_names = (allegheny_full.loc[allegheny_full['tract']
                                     .isin( tract_count
                                           .loc[tract_count['municipality']>1,:]
                                           .index.to_list())]
                                           .sort_values(by='tract'))
borough_dict = dict(zip(updated_borough_names.tract.values,
                        updated_borough_names.municipality.values))
full_reference = pd.merge(original_names,
                          updated_borough_names,
                          on='tract').rename(columns={'municipality_y':'municipality',
                                                      'municipality_x':'NAME'})
short_reference = full_reference.drop(columns=['tract']).drop_duplicates()
short_dict= dict(zip(short_reference.NAME.values, short_reference.municipality.values))
## Remove duplicate tracts from allegheny full and replace with condensed version
allegheny_full = allegheny_full[~allegheny_full['tract'].isin(borough_dict.keys())]
allegheny_name_tract_mapping = pd.concat([allegheny_full,
                                          pd.DataFrame( {'municipality':borough_dict.values(),
                                                         'tract':borough_dict.keys()})])

# add condensed municipality names to original shape file
allegheny_shapes['NAME_TRACT'] = (allegheny_shapes
                                  .NAME
                                  .apply(lambda x:
                                         short_dict[x] if x in(short_dict.keys()) else x ))
allegheny_shapes.sort_values(by=['NAME_TRACT'], inplace=True)
descriptive_shape_data_raw = allegheny_shapes[['NAME_TRACT', 'TYPE',
                                               'COG', 'SCHOOLD',
                                               'CONGDIST',  'REGION',
                                               'CNTL_ID', 'CNTYCOUNCI',
                                               'ASSESSORTE']]
# retain first row of each municipality instance
descriptive_shape_data = descriptive_shape_data_raw.groupby('NAME_TRACT').first()

# merge municpality shapes that share a census tract
geometry_shape_data_raw = allegheny_shapes[['NAME_TRACT', 'geometry']]
allegheny_shapes_cleaned = geometry_shape_data_raw.dissolve(by='NAME_TRACT')

# combine new shape data with reduced data originally paired with the shape file
allegheny_shapes_desc = pd.merge(descriptive_shape_data,
                                 allegheny_shapes_cleaned,
                                 on='NAME_TRACT').reset_index()


allegheny_pop['tract'] = allegheny_pop['tract'].str.strip()
allegheny_name_tract_mapping['tract'] = allegheny_name_tract_mapping['tract'].str.strip()
############
allegheny_tract_w_muni = pd.merge(allegheny_pop,
                                  allegheny_name_tract_mapping,
                                  on='tract',
                                  how='left')
allegheny_tract_w_muni.dropna(inplace=True)
allegheny_tract_w_muni.to_pickle('data_files/track_data_pre_agg.pkl')
