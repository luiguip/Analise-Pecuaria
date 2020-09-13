#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

#%%
df_cnpjs = pd.read_csv('cnpjs_cnaes_bovinos.csv', index_col=[0])

print(df_cnpjs.info())

#%%

df_exp = pd.read_csv('exp_bovinos.csv', index_col=[0])

print(df_exp)

#%%
sum_nans = df_cnpjs.isna().sum()
print(sum_nans[sum_nans != 0])

#%%

drop_nans = sum_nans[sum_nans > 100000].index.to_list()
print(drop_nans)
#%%

df_cnpjs = df_cnpjs.drop(drop_nans, axis=1)

#%%

sum_nans = df_cnpjs.isna().sum()
print(sum_nans[sum_nans != 0])

#%%

drop_nan_non_used = ['numero', 'bairro', 'ddd_telefone_1', 'correio_eletronico', 'descricao_tipo_logradouro']
df_cnpjs = df_cnpjs.drop(drop_nan_non_used, axis=1)

#%%

df_cnpjs.info()

#%%

drop_non_used = ['logradouro', 'cep', 'codigo_municipio', 'municipio']
df_cnpjs = df_cnpjs.drop(drop_non_used, axis=1)

#%%

sum_nans = df_cnpjs.isna().sum()
print(sum_nans[sum_nans != 0])

#%%

print(df_cnpjs['opcao_pelo_mei'].value_counts())

#%%
df_cnpjs['opcao_pelo_mei'] = df_cnpjs['opcao_pelo_mei'].fillna('OUTROS')
print(df_cnpjs['opcao_pelo_mei'].value_counts())

#%%
df_cnpjs[['porte_empresa']].info()
print(df_cnpjs['porte_empresa'].value_counts())
#%%
#Fonte: Tiago Baroni
df_cnpjs['porte_empresa_desc'] = df_cnpjs['porte_empresa'].replace([0, 1 ,3 ,5],['NAO INFORMADO', 'MICRO EMPRESA','EMPRESA DE PEQUENO PORTE','DEMAIS'])
print(df_cnpjs['porte_empresa_desc'].value_counts())

#%%

df_cnpjs[['situacao_cadastral']].info()
print(df_cnpjs['situacao_cadastral'].value_counts())

#%%

df_cnpjs = df_cnpjs[df_cnpjs['situacao_cadastral'].isin([8,2])]
print(df_cnpjs['situacao_cadastral'].value_counts())
#%%
#Fonte: Tiago Baroni
df_cnpjs['situacao_atividade']= df_cnpjs['situacao_cadastral'].replace([8 ,2],['INATIVA','ATIVA'])
print(df_cnpjs['situacao_atividade'].value_counts())
#%%

print(df_cnpjs.info())

#%%

print(df_cnpjs['opcao_pelo_simples'].value_counts())

#%%
simples_descs = ['NAO OPTANTE', 'OPTANTE', 'OPTANTE', 'EXCLUIDO', 'EXCLUIDO']
df_cnpjs['opcao_pelo_simples_desc'] = df_cnpjs['opcao_pelo_simples'].replace([0, 5, 7, 6, 8], simples_descs)
print(df_cnpjs['opcao_pelo_simples_desc'].value_counts())


#%%

print(df_cnpjs[['data_situacao_cadastral', 'data_inicio_atividade']].head())

#%%

df_cnpjs.to_csv('cnpjs_bovinos_preprocessados.csv')