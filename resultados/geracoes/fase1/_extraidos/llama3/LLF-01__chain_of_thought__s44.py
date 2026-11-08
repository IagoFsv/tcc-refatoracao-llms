import pandas as pd


def get_last_word(description):
    return description.split()[-1]


def get_second_last_word(description):
    return description.split()[-2]


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    # split the description column and get the last word
    df['City'] = df['Description'].str.lower().str.split().apply(get_last_word)
    # check if the last word in the description is in the city list
    df['City'] = df['City'].apply(lambda x: x if x.lower() in city_list else 'Unknown')
    # check the last 2 words in the descirption if the city columns is unknown
    df['City'] = df.apply(get_city, axis=1)
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def get_city(row):
    city = row['City']
    if city == 'Unknown':
        description = row['Description']
        second_last_word = get_second_last_word(description)
        if second_last_word.lower() in city_list:
            return second_last_word.title()
    return city


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
