import pandas as pd

def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    city_list = [city.lower() for city in city_list]

    def get_city_from_description(description):
        description_parts = description.lower().split()
        if description_parts[-1] in city_list:
            return description_parts[-1]
        if description_parts[-2] in city_list:
            return description_parts[-2]
        return 'Unknown'

    df['City'] = df['Description'].apply(get_city_from_description)
    df['City'] = df['City'].str.title()
    return df

def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
