import pandas as pd


def get_last_word(description):
    """Get the last word of a description"""
    return description.lower().split()[-1]


def get_city_from_description(description, city_list):
    """Get the city from a description"""
    last_word = get_last_word(description)
    return last_word if last_word in city_list else 'Unknown'


def get_second_last_word(description):
    """Get the second last word of a description"""
    return description.lower().split()[-2]


def get_city_from_description_unknown(description, city_list):
    """Get the city from a description when the city is unknown"""
    last_word = get_last_word(description)
    if last_word == 'Unknown':
        second_last_word = get_second_last_word(description)
        return second_last_word.lower() if second_last_word.lower() in city_list else 'Unknown'
    return last_word


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    df['City'] = df['Description'].apply(get_city_from_description, args=(city_list,))
    df['City'] = df['City'].apply(lambda x: x.title())
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
