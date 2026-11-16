import pandas as pd

def extract_last_word(description, city_list):
    description = description.lower().split()
    if description[-1] in city_list:
        return description[-1]
    if len(description) > 1 and description[-2].lower() in city_list:
        return description[-2]
    return 'Unknown'

def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    # split the description column and get the last word
    df['City'] = df['Description'].apply(lambda x: extract_last_word(x, city_list))
    # make city title case
    df['City'] = df['City'].str.title()
    return df

def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
