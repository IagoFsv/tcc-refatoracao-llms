import pandas as pd

def get_city_from_description(description):
    """Get the city from a description"""
    return description.split()[-1].lower()

def get_city_from_description_with_fallback(description, city_list):
    """Get the city from a description with fallback to the last 2 words"""
    city = get_city_from_description(description)
    if city == 'Unknown':
        city = description.split()[-2].lower()
        if city in city_list:
            return city
    return city

def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    df['City'] = df['Description'].str.lower().apply(get_city_from_description)
    df['City'] = df.apply(get_city_from_description_with_fallback, args=(city_list,), axis=1)
    df['City'] = df['City'].str.title()
    return df

def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
