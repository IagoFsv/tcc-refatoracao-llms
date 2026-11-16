import pandas as pd


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    city_list = [city.lower() for city in city_list]
    df['Description'] = df['Description'].str.lower()

    def get_city(row):
        words = row['Description'].split()
        if words:
            city = words[-1].lower()
            if city in city_list:
                return city
            elif len(words) > 1 and words[-2].lower() in city_list:
                return words[-2].lower()
            else:
                return 'Unknown'

    df['City'] = df.apply(get_city, axis=1)
    df['City'] = df['City'].str.title()
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
