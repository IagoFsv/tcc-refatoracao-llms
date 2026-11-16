import pandas as pd

def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    city_list = [city.lower() for city in city_list]
    
    def get_last_word(city_desc):
        return city_desc.lower().split()[-1]
    
    def get_second_last_word(city_desc):
        return city_desc.lower().split()[-2]
    
    df['City'] = df['Description'].apply(get_last_word)
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    df['City'] = df.apply(lambda x: get_second_last_word(x['Description']) if x['City'] == 'Unknown' and get_second_last_word(x['Description']) in city_list else x['City'], axis=1)
    df['City'] = df['City'].str.title()
    return df

def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
