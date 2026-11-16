import pandas as pd


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    city_list = [city.lower() for city in city_list]
    df['Description'] = df['Description'].str.lower()
    df['City'] = df['Description'].str.split().apply(lambda x: x[-1])
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')

    def check_city(row):
        if row['City'] == 'Unknown':
            desc = row['Description'].split()
            if desc[-2].lower() in city_list:
                return desc[-2].lower()
            else:
                return 'Unknown'
        else:
            return row['City']

    df['City'] = df.apply(check_city, axis=1)
    df['City'] = df['City'].str.title()
    return df


def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
