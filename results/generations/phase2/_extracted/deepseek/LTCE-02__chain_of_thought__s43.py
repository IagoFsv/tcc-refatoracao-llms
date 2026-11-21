import pandas as pd


def update_city_column(df, city_list):
    city_list = [city.lower() for city in city_list]
    df['City'] = df['Description'].str.lower().str.split().apply(lambda x: x[-1])
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    df['City'] = df.apply(lambda x: x['City'] if x['City'] in city_list else 'Unknown', axis=1)
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and x['Description'].split()[-2].lower() in city_list else x['City'], axis=1)
    df['City'] = df['City'].str.title()
    return df


def run(descriptions, cities):
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
