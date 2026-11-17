import pandas as pd

def split_description(description):
    return description.lower().split()

def get_last_word(description_split):
    return description_split[-1]

def check_if_in_city_list(city, city_list):
    return city if city in city_list else 'Unknown'

def check_last_2_words(description_split, city, city_list):
    if city == 'Unknown' and description_split[-2].lower() in city_list:
        return description_split[-2].lower()
    else:
        return city

def make_city_title_case(city):
    return city.title()

def update_city_column(df, city_list):
    city_list = [city.lower() for city in city_list]
    df['City'] = df['Description'].apply(split_description).apply(get_last_word)
    df['City'] = df['City'].apply(lambda city: check_if_in_city_list(city, city_list))
    df['City'] = df.apply(lambda x: check_last_2_words(split_description(x['Description']), x['City'], city_list), axis=1)
    df['City'] = df['City'].apply(make_city_title_case)
    return df

def run(descriptions, cities):
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
