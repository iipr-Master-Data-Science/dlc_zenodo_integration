#!/usr/local/lib/python3.7/virtual-envs/my-py-3.7/bin/python

import sys
print(sys.version)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

fname = sys.argv[1]
# Posible values for countries:
#['AT' 'BE' 'BG' 'CH' 'CY' 'CZ' 'DE' 'DK' 'EA17' 'EA18' 'EA19' 'EE' 'EL'
# 'ES' 'EU15' 'EU27' 'EU28' 'FI' 'FR' 'HR' 'HU' 'IE' 'IS' 'IT' 'LT' 'LU'
# 'LV' 'ME' 'MK' 'MT' 'NL' 'NO' 'PL' 'PT' 'RO' 'RS' 'SE' 'SI' 'SK' 'TR'
# 'UK']
country_1 = sys.argv[2]
country_2 = sys.argv[3]
country_3 = sys.argv[4]
# Possible values for age range:
#['Y15-19' 'Y15-24' 'Y15-39' 'Y15-59' 'Y15-64' 'Y15-74' 'Y20-24' 'Y20-64'
# 'Y25-29' 'Y25-49' 'Y25-54' 'Y25-59' 'Y25-64' 'Y25-74' 'Y30-34' 'Y35-39'
# 'Y40-44' 'Y40-59' 'Y40-64' 'Y45-49' 'Y50-54' 'Y50-59' 'Y50-64' 'Y50-74'
# 'Y55-59' 'Y55-64' 'Y60-64' 'Y65-69' 'Y65-74' 'Y70-74']
ages = sys.argv[5]
# Possible values for educational level:
#['ED0-2' 'ED3_4' 'ED5-8' 'NRP' 'TOTAL']
edu = sys.argv[6]


################################################
#
#            Load and prepare data
#
################################################

# Load TSV
df = pd.read_csv(fname, sep='\t')
# Split column with multiple values
df[['unit','sex','age','isced11','geo']] = df.iloc[:, 0].str.split(',', expand=True)
cols = df.columns.tolist()
# Reorder and strip columns
# Also, get rid of 'unit' column (doesn't add information)
df = df[['sex', 'age', 'isced11', 'geo'] + cols[1:-5]]
df.columns = ['Y' + str.strip(c) if 'Q' in c else c for c in df.columns]
# Remove characters and cast to float
df.loc[0:,'Y2018Q3':'Y1998Q1'] = df.loc[:,'Y2018Q3':'Y1998Q1'].replace(r'[^0-9.\-]', '', regex=True)
df.loc[0:,'Y2018Q3':'Y1998Q1'] = df.loc[:,'Y2018Q3':'Y1998Q1'].replace('', np.nan,)
df[df.columns[4:]] = df[df.columns[4:]].astype(float)
print('Sexs:', df.sex.unique())
print('Geos:', df.geo.unique())
print('Age ranges:', df.age.unique())
print('Educational levels:', df.isced11.unique())
#print(df.head())

# Set index
df.set_index(['sex', 'age', 'isced11', 'geo'], inplace=True)
# Damos la vuelta a las columnas para obtener un orden cronológico:
df = df[df.columns[::-1]]

df_bar = df.copy()
# Renombramos las columnas para poder hacer el group_by:
df_bar.columns = [y[1:5] for y in df.head().columns]
df_bar = df_bar.groupby(level=0, axis=1).mean()
df_bar.head()


################################################
#
#            Plot histograms
#
################################################

fig, (ax0, ax1) = plt.subplots(1, 2)
fig.set_size_inches(10, 10)
fig.tight_layout()
fig.subplots_adjust(wspace=0.135)
# Ancho para tener más de una barra por año:
width = 0.25
ind = np.arange(len(df_bar.columns))

geos = [country_1, country_2, country_3]
sex = ['F', 'M', 'T']

# Mapeamos colores a paises:
# Otros: ['purple', 'orange', 'magenta', 'green', 'yellow', 'blue', 'red', 'black']
colors = ['purple', 'magenta', 'red']
map_cols = dict(zip(geos, colors))
years = range(1998, 2019)

# Hay que invertir el eje x del plot de la izquierda
ax0.invert_xaxis()
ax0.yaxis.tick_right()
# Titulos, ticks, sus posiciones...
ax0.set_title('Employed female [%], ages: {}'.format(ages[1:]), fontsize=15)
ax1.set_title('Employed male [%], ages: {}'.format(ages[1:]), fontsize=15)
ax0.yaxis.set_major_locator(mticker.NullLocator())
ax1.yaxis.set_major_locator(mticker.NullLocator())
ax0.tick_params(axis=u'y', which=u'major', length=0)
ax1.tick_params(axis=u'y', which=u'major', length=0)
ax0.tick_params(axis=u'both', which=u'major', labelsize=14)
ax1.tick_params(axis=u'both', which=u'major', labelsize=14)

# Y añadimos las barras en el plot correspondiente:
ax0.barh(ind, df_bar.loc['F', ages, edu, country_1], 
         width, facecolor=map_cols[country_1], alpha=0.7, edgecolor='white')
ax0.barh(ind + width, df_bar.loc['F', ages, edu, country_2], 
         width, facecolor=map_cols[country_2], alpha=0.7, edgecolor='white')
ax0.barh(ind + 2*width, df_bar.loc['F', ages, edu, country_3], 
         width, facecolor=map_cols[country_3], alpha=0.7, edgecolor='white')
ax1.barh(ind, df_bar.loc['M', ages, edu, country_1], 
         width, facecolor=map_cols[country_1], alpha=0.7, edgecolor='white')
ax1.barh(ind + width, df_bar.loc['M', ages, edu, country_2], 
         width, facecolor=map_cols[country_2], alpha=0.7, edgecolor='white')
ax1.barh(ind + 2*width, df_bar.loc['M', ages, edu, country_3], 
         width, facecolor=map_cols[country_3], alpha=0.7, edgecolor='white')
# Por último añadimos los años en el eje y:
y_pos = range(0, 22)
for idx, year in enumerate(years):
    ax0.text(-0.6, y_pos[idx]+0.1, year, fontsize=14)

ax0.legend([country_1, country_2, country_3], loc='best', fontsize=15)
plt.show()