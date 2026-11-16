import pandas as pd

def update_city_column(df, city_list):
    city_list = [city.lower() for city in city_list]
    df['City'] = df['Description'].str.lower().str.split().apply(get_last_word)
    df['City'] = df['City'].apply(check_city, args=(city_list,))
    df['City'] = df.apply(check_second_last_word, args=(city_list,), axis=1)
    df['City'] = df['City'].str.title()
    return df

def get_last_word(x):
    return x[-1]

def check_city(x, city_list):
    return x if x in city_list else 'Unknown'

def check_second_last_word(x, city_list):
    if x['City'] == 'Unknown':
        second_last_word = x['Description'].split()[-2].lower()
        return second_last_word if second_last_word in city_list else 'Unknown'
    return x['City']

def executar(descricoes, cidades):
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
