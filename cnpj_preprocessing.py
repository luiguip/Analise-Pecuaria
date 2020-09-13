#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sqlite3
import pandas as pd
#%%
con = sqlite3.connect('amostra100pc.sqlite')

#%%
tables = pd.read_sql_query("SELECT * from sqlite_master", con)
print(tables)

#Utilizar a tabela do cnae para selecionar os cpnjs que se relacionam a gado,
# aves, milho, soja
#%%

df_cnae = pd.read_sql_query('select * from tab_cnae', con)
print(df_cnae.info())

#%%

mask = (df_cnae['cod_secao'] == 'A') & (df_cnae['cod_divisao'] == '01')
df_cnae_agropec = df_cnae[mask]
print(df_cnae_agropec.head())

#%%
def cnae_names(pattern):
    mask = df_cnae['nm_cnae'].str.contains(pattern, flags=re.IGNORECASE)
    return df_cnae[mask]

#%%
print(cnae_names('milho')['nm_cnae'])

df_cnae_filtered = cnae_names('Cultivo de milho')

print(df_cnae_filtered)

#%%
print(cnae_names('soja')['nm_cnae'])

df_cnae_filtered = pd.concat([df_cnae_filtered, cnae_names('Cultivo de soja')])
df_cnae_filtered = pd.concat([df_cnae_filtered, cnae_names('Comércio atacadista de soja')])

print(df_cnae_filtered)

#%%
print(cnae_names('bovino')['nm_cnae'])

df_cnae_filtered = pd.concat([df_cnae_filtered,
                              cnae_names('Criação de bovinos para corte')])

df_cnae_filtered = pd.concat([df_cnae_filtered,
                              cnae_names('Frigorífico - abate de bovinos')])

print(df_cnae_filtered)

#%%

df_cnae_filtered.to_csv('cnaes.csv')

#%%

print(cnae_names('bovino')[['cod_cnae', 'nm_cnae']])

cod_bovino_corte = '0151201'
cod_bovino_frigorifico = '1011201'
#%%

df_cnpjs = pd.read_sql_query(
    "SELECT * from cnpj_dados_cadastrais_pj where cnae_fiscal in ('{0}', '{1}')".format(cod_bovino_corte, cod_bovino_frigorifico), con)
print(df_cnpjs.info())

#%%

print(df_cnpjs.isna().sum())

#%%

print(df_cnpjs['cnae_fiscal'].head())

#%%

print(df_cnae_filtered['cod_cnae'])

#%%

df_cnpjs_cnaes = df_cnpjs.join(df_cnae_filtered.set_index('cod_cnae'), on='cnae_fiscal')
df_cnpjs_cnaes = df_cnpjs_cnaes.dropna(subset=['cnae_fiscal'] ,axis=0)
print(df_cnpjs_cnaes.info())


#%%

df_bovinos = df_cnpjs_cnaes[df_cnpjs_cnaes['cnae_fiscal'].isin(
    [cod_bovino_corte, cod_bovino_frigorifico])]
# Criar tabela de bovinos para integrar com os outros dados.
#%%

df_bovinos.to_csv('cnpjs_cnaes_bovinos.csv')