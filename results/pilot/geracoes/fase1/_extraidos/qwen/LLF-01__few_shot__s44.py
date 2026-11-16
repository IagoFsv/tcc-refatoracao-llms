import pandas as pd

def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    city_list = [city.lower() for city in city_list]
    df['City'] = df['Description'].str.lower().str.split().apply(get_last_word)
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and x['Description'].split()[-2].lower() in city_list else x['City'], axis=1)
    df['City'] = df['City'].str.title()
    return df

def get_last_word(x):
    return x[-1]

def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
