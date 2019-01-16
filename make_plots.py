#!/usr/local/lib/python3.7/virtual-envs/my-py-3.7/bin/python

import sys
print(sys.version)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Load TSV
df = pd.read_csv('./lfsq_ergaed.tsv', sep='\t')
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

fig, (ax0, ax1) = plt.subplots(1, 2)
fig.set_size_inches(10, 10)
fig.tight_layout()
fig.subplots_adjust(wspace=0.135)
# Ancho para tener más de una barra por año:
width = 0.25
ind = np.arange(len(df_bar.columns))

geos = ['ES', 'PT', 'DE', 'IT', 'FR', 'UK', 'EU28', 'EA19']
ages = ['Y_GE15', 'Y25-64']
sex = ['F', 'M', 'T']

# Mapeamos colores a paises:
colors = ['purple', 'orange', 'magenta', 'green', 'yellow', 'blue', 'red', 'black']
map_cols = dict(zip(geos, colors))
# Mapeamos los rangos de edad para que sean más legibles
age_range = ['≥15', '[25-64]']
map_ages = dict(zip(ages, age_range))
years = range(1998, 2019)

# Hay que invertir el eje x del plot de la izquierda
ax0.invert_xaxis()
ax0.yaxis.tick_right()
# Titulos, ticks, sus posiciones...
ax0.set_title('Employed female [%], ages: [25-64]', fontsize=15)
ax1.set_title('Employed male [%], ages: [25-64]', fontsize=15)
ax0.yaxis.set_major_locator(mticker.NullLocator())
ax1.yaxis.set_major_locator(mticker.NullLocator())
ax0.tick_params(axis=u'y', which=u'major', length=0)
ax1.tick_params(axis=u'y', which=u'major', length=0)
ax0.tick_params(axis=u'both', which=u'major', labelsize=14)
ax1.tick_params(axis=u'both', which=u'major', labelsize=14)

# Y añadimos las barras en el plot correspondiente:
ax0.barh(ind, df_bar.loc['F', 'Y25-64', 'TOTAL', 'DE'], 
         width, facecolor=map_cols['DE'], alpha=0.7, edgecolor='white')
ax0.barh(ind + width, df_bar.loc['F', 'Y25-64', 'TOTAL', 'ES'], 
         width, facecolor=map_cols['ES'], alpha=0.7, edgecolor='white')
ax0.barh(ind + 2*width, df_bar.loc['F', 'Y25-64', 'TOTAL', 'EU28'], 
         width, facecolor=map_cols['EU28'], alpha=0.7, edgecolor='white')
ax1.barh(ind, df_bar.loc['M', 'Y25-64', 'TOTAL', 'DE'], 
         width, facecolor=map_cols['DE'], alpha=0.7, edgecolor='white')
ax1.barh(ind + width, df_bar.loc['M', 'Y25-64', 'TOTAL', 'ES'], 
         width, facecolor=map_cols['ES'], alpha=0.7, edgecolor='white')
ax1.barh(ind + 2*width, df_bar.loc['M', 'Y25-64', 'TOTAL', 'EU28'], 
         width, facecolor=map_cols['EU28'], alpha=0.7, edgecolor='white')
# Por último añadimos los años en el eje y:
y_pos = range(0, 22)
for idx, year in enumerate(years):
    ax0.text(-0.6, y_pos[idx]+0.1, year, fontsize=14)

ax0.legend(['DE', 'ES', 'EU28'], loc='best', fontsize=15)
plt.show()