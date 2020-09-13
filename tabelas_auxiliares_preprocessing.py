#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import pandas as pd

#%%

tabelas_auxiliares = 'tabelas_auxiliares.xlsx'

#%%
df_indice = pd.read_excel(tabelas_auxiliares, sheet_name='ÍNDICE')

print(df_indice.info())
#%%

print(df_indice.iloc[:,0:2])

#%%
sheet_sh = '1'
sheet_paises = '11'
sheet_muns = '14'
# Aba 1 SH - SH4.
# Aba 11 Paises.
# Aba 14 Municipios.

#%%

df_sh = pd.read_excel(tabelas_auxiliares, sheet_name=sheet_sh)



print(df_sh.info())

# tabela de exportacoes utiliza sh4
#%%

df_sh = df_sh[['CO_SH4', 'NO_SH4_POR']]
print(df_sh.head())

# Agora temos código e descricao.
#%%

description_series = df_sh['NO_SH4_POR']

def get_regex_rows(reg):
    return description_series.str.contains(reg, flags=re.IGNORECASE)

def show_regex_rows(reg):
    regex_rows = get_regex_rows(reg)
    print(description_series[regex_rows].unique())


#%%

#Bovinos

show_regex_rows('bovino')

# Bovinos não retornou os valores desejados

#%%

show_regex_rows('carne')

# Retoronou resultados mais satisfatorios. Como peixes tem uma linha, carne bovina deve ter tambem.
# Comentario feito antes de utilizar o IGNORECASE
#%%

show_regex_rows('bovin')

bovino_vivo = 'Animais vivos da espécie bovina'

df_sh_selected_rows = df_sh[get_regex_rows(bovino_vivo)].drop_duplicates()

# Encontrado!
# Vou focar nas carnes frescas, refrigeradas ou congeladas que são o principal
# produto do gado de corte.
#%%

def add_rows(pattern):
    df_to_add = df_sh[get_regex_rows(pattern)].drop_duplicates()
    return pd.concat([df_sh_selected_rows, df_to_add])

#%%
carne_bovina_regex = 'Carnes de animais da espécie bovina'

show_regex_rows(carne_bovina_regex)

df_sh_selected_rows = add_rows(carne_bovina_regex)

print(df_sh_selected_rows)
#%%

#Aves

show_regex_rows('carne')

# Carne de aves da posicao sh4 00105

#%%


print(df_sh[df_sh['CO_SH4'] == 105]['NO_SH4_POR'].unique())

df_sh_selected_rows = pd.concat([df_sh_selected_rows, 
                                 df_sh[df_sh['CO_SH4'] == 105]
                                 .drop_duplicates()])

print(df_sh_selected_rows)
# Certo então são as carnes das aves desse sh4. 
#%%

descricao_carne_aves = 'Carnes e miudezas comestíveis, frescas, refrigeradas ou congeladas, das aves'

df_sh_selected_rows = add_rows(descricao_carne_aves)

print(df_sh_selected_rows)
#%%

#Soja

show_regex_rows('soja')
soja = 'Soja, mesmo triturada'
df_sh_selected_rows = add_rows(soja)

print(df_sh_selected_rows)

#%%

#Milho

show_regex_rows('milho')
milho = 'Milho'
df_sh_selected_rows = pd.concat([df_sh_selected_rows, 
                                 df_sh[df_sh['NO_SH4_POR'] == milho]
                                 .drop_duplicates()])
print(df_sh_selected_rows)

#%%

df_sh_selected_rows.to_csv('sh4.csv')

#%%

df_pais = pd.read_excel(tabelas_auxiliares, sheet_name=sheet_paises)
print(df_pais.info())

#%%

print(df_pais.iloc[0:2, 0:4])

#%%

print(df_pais.iloc[:, 0:2].describe())

#O código maximo da tabela de exportacoes coincide com a CO_PAIS

#%%

df_pais = df_pais[['CO_PAIS', 'NO_PAIS']]
print(df_pais.head())

#%%

df_pais.to_csv('pais.csv')