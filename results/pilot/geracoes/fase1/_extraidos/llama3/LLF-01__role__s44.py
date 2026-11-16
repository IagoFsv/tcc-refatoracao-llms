import pandas as pd


def convert_to_lower(city_list):
    """Convert all text in city_list to lower case"""
    return [city.lower() for city in city_list]


def get_last_word(description):
    """Split the description column and get the last word"""
    return description.lower().str.split().apply(lambda x: x[-1])


def get_city(description, city_list):
    """Check if the last word in the description is in the city list"""
    return description if description in city_list else 'Unknown'


def get_city_from_description(description, city_list):
    """Check the last 2 words in the description if the city column is unknown"""
    last_two_words = description.split()[-2].lower()
    return last_two_words if last_two_words in city_list else 'Unknown'


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    df['City'] = df['Description'].apply(get_last_word)
    df['City'] = df.apply(lambda x: get_city(x['City'], city_list) if x['City'] == 'Unknown' else x['City'], axis=1)
    df['City'] = df['City'].str.title()
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
