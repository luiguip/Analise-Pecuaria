#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

#%%

df = pd.read_csv('EXP_COMPLETA_MUN.csv', sep=';')

print(df.info())

#%%

print(df.isna().sum())
#%%

df_sh = pd.read_csv('sh4.csv').drop(['Unnamed: 0'], axis=1)
print(df_sh.info())

#%%

print(df[df['SH4'].isin(df_sh['CO_SH4'].to_list())]['SH4'].value_counts())
#%%

df_pais = pd.read_csv('pais.csv').drop(['Unnamed: 0'], axis=1)
print(df_pais.info())
#%%
df = df.drop(['CO_MUN'], axis=1)
print(df.head())

#%%

df_with_sh4 = df.join(df_sh.set_index('CO_SH4'), on='SH4')
df_with_sh4 = df_with_sh4.dropna(axis=0)
print(df_with_sh4.head())

#%%

print(df_with_sh4[['SH4', 'NO_SH4_POR']].value_counts())

#%%

df_complete = df_with_sh4.join(df_pais.set_index('CO_PAIS'), on='CO_PAIS')
df_complete = df_complete
print(df_complete)

#%%

print(df_complete[['CO_PAIS', 'NO_PAIS']].value_counts().head())

#%%

print(df_complete.size)
#%%

print(df_complete[df_complete['NO_PAIS'] == 'Brasil'])

#Exsitem 5 casos de exportação do Brasil ao Brasil. pode ser um erro ou uma
# situação especial.

df_complete = df_complete[df_complete['NO_PAIS'] != 'Brasil']
print(df_complete[df_complete['NO_PAIS'] == 'Brasil'])
#%%

print(df_complete['VL_FOB'].describe())

#Exitem esportações de 0 dolares. O que é uma anormalidade.

print(df_complete[df_complete['VL_FOB'] == 0].count())

#39 registros com valor de venda 0. 

df_complete = df_complete[df_complete['VL_FOB'] != 0]
#%%

df_complete.to_csv('exp_completa.csv')

#%%

print(df_complete[['SH4', 'NO_SH4_POR']].value_counts())
#%%

df_bovinos_corte = df_complete[df_complete['SH4'].isin(['201', '202'])]
print(df_bovinos_corte.info())

#%%

df_bovinos_corte.to_csv('exp_bovinos.csv')