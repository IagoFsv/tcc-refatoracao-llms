def update_city_column(df, city_list):
    city_list = [city.lower() for city in city_list]
    df['City'] = df['Description'].apply(get_last_word)
    df['City'] = df['City'].apply(lambda x: check_city(x, city_list))
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and x['Description'].split()[-2].lower() in city_list else x['City'], axis=1)
    df['City'] = df['City'].str.title()
    return df
