import pandas as pd


def get_last_word(description):
    """Extract the last word from the description."""
    return description.lower().split()[-1]


def get_second_last_word(description):
    """Extract the second last word from the description."""
    return description.lower().split()[-2]


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    
    # Update the 'City' column using the helper functions
    df['City'] = df['Description'].apply(get_last_word)
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    df['City'] = df.apply(lambda x: get_second_last_word(x['Description']) if x['City'] == 'Unknown' and get_second_last_word(x['Description']) in city_list else x['City'], axis=1)
    
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
