"""
exploration of census tracts data
"""
import wget

DATA_URL = 'https://raw.githubusercontent.com/aapeebles/iteam_exercise/refs/heads/main/data_files/Data%20exercise%20data%20-%20Sheet1.csv'
SHAPEFILE_URL = 'https://www.pasda.psu.edu/download/census/cb_2015_42_tract_500k.zip'

file_Path = 'data_files/census_data.csv'
shapefile_name = 'data_files/cb_2015_42_tract_500k.zip'
wget.download(SHAPEFILE_URL, shapefile_name)
print('downloaded')

wget.download(DATA_URL, file_Path)
print('downloaded')

import pandas as pd
vulnerable = pd.read_csv(DATA_URL, dtype = {"FIPS Code":"object"})
vulnerable.dtypes
allegheny = vulnerable.loc[(vulnerable.State.str.contains('Pennsylvania')) & (vulnerable.County.str.contains('Allegheny County')),:]
allegheny.shape

from pygris import counties
import geopandas as gpd
from geodatasets import get_path
import contextily as cx
from matplotlib import pyplot as plt
import mpl_toolkits as mpl


us_counties = counties(cb = True, year = 2020)
us_counties.head()

pgh_tract = gpd.read_file('data_files/Census_Tract_2020_pgh.zip')
pgh_tract = pgh_tract.to_crs(epsg = 32617)
print(pgh_tract.head(2))
pgh_tract.head()

print('Shape: ', pgh_tract.shape)
print("\nThe shapefile projection is: {}".format(pgh_tract.crs))

allegheny.rename(columns={'FIPS Code':'GEOID'}, inplace=True)
pgh_tract.rename(columns={'geoid':'GEOID'}, inplace=True)
allegheny.columns


pa_merge = pgh_tract.merge(allegheny, on='GEOID', how='inner')
pa_merge.columns

pa_merge['BIPOC % POP'] = pa_merge['BIPOC Residents'] /pa_merge['Population']



fig, ax = plt.subplots(1, 1, figsize = (20, 10))


import matplotlib.pyplot as plt
from pygris import 



#http://server.arcgisonline.com/arcgis/rest/services
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

plt.show()

# Plot data
# Source: https://geopandas.readthedocs.io/en/latest/docs/user_guide/mapping.html
ax = pa_merge.plot(column = "BIPOC % POP",
                       figsize=(10, 10),
                       cmap = "RdPu",
                       legend = True,
                       alpha=0.5)
cx.add_basemap(ax, cx.sources.ST_TONER_LITE)

# Stylize plots


# Set title
ax.set_title('BIPOC percent by census tract in Pittsburgh', fontdict = {'fontsize': '25', 'fontweight' : '3'})
plt.show()
