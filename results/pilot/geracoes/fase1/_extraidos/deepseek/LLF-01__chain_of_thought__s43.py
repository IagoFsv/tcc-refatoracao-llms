import pandas as pd


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    # split the description column and get the last word
    df['City'] = df['Description'].str.lower().str.split().apply(get_last_word)
    # check if the last word in the description is in the city list
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    # check the last 2 words in the descirption if the city columns is unknown. Compare the 2 words to the city list for a match. If there is a match, add the city name to the city column
    df['City'] = df.apply(check_unknown_city, axis=1)
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def get_last_word(description):
    """Return the last word from the description"""
    return description[-1]


def check_unknown_city(row):
    """Check if the city column is unknown and replace it with the last 2 words from the description if they are in the city list"""
    if row['City'] == 'Unknown':
        description_words = row['Description'].split()
        last_word = description_words[-2].lower()
        if last_word in city_list:
            return last_word
    return row['City']


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
