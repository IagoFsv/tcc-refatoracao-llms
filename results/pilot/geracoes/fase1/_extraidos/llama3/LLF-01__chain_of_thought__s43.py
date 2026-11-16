import pandas as pd


def get_last_word(description):
    """Return the last word of a description"""
    return description.split()[-1]


def get_city_from_description(description, city_list):
    """Return the city from a description or 'Unknown' if not found"""
    return description.lower() if description.lower() in city_list else 'Unknown'


def update_city(description, city_list):
    """Update the city column based on the description"""
    if description['City'] == 'Unknown':
        last_word = get_last_word(description['Description'])
        if get_city_from_description(last_word, city_list) in city_list:
            return last_word.lower()
    return description['City']


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    df['City'] = df['Description'].str.lower().apply(get_last_word)
    df['City'] = df['City'].apply(update_city, args=(city_list,))
    df['City'] = df['City'].str.title()
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
