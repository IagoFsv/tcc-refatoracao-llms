"""Coluna de cidade a partir da descricao de transacoes bancarias.

Ponto de entrada publico: executar(descricoes, cidades). Nao altere o nome nem
a assinatura dessa funcao; o restante do arquivo pode ser reorganizado
livremente.
"""

import pandas as pd


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    # split the description column and get the last word
    df['City'] = df['Description'].str.lower().str.split().apply(lambda x: x[-1])
    # check if the last word in the description is in the city list
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    # TODO: this check for city looks like its only checking second last word (see: Abu Dhabi)
    # check the last 2 words in the descirption if the city columns is unknown. Compare the 2 words to the city list for a match. If there is a match, add the city name to the city column
    # df['City'] = df['City'].apply(lambda x: x if x != 'Unknown' else df['Description'].str.lower().str.split().apply(lambda x: x[-2]) if df['Description'].str.lower().str.split().apply(lambda x: x[-2]) in city_list else 'Unknown')
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and x['Description'].split()[-2].lower() in city_list else x['City'], axis=1)
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
