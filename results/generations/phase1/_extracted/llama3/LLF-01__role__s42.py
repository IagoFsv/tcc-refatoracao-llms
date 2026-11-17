"""City column from the description of bank transactions.

Public entry point: run(descriptions, cities). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import pandas as pd


def convert_to_lower(city_list):
    """Convert all text in city_list to lower case"""
    return [city.lower() for city in city_list]


def get_last_word(description):
    """Split the description column and get the last word"""
    return description.lower().split()[-1]


def check_city(city, city_list):
    """Check if the last word in the description is in the city list"""
    return city if city in city_list else 'Unknown'


def get_second_last_word(description, city_list):
    """Get the second last word and check if it's in the city list"""
    second_last_word = description.lower().split()[-2]
    return second_last_word if second_last_word in city_list else 'Unknown'


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    df['City'] = df['Description'].apply(get_last_word)
    df['City'] = df['City'].apply(check_city, args=(city_list,))
    df['City'] = df.apply(lambda x: get_second_last_word(x['Description'], city_list) if x['City'] == 'Unknown' else x['City'], axis=1)
    df['City'] = df['City'].str.title()
    return df


def run(descriptions, cities):
    """Classifies the descriptions. Public entry point of this unit."""
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
