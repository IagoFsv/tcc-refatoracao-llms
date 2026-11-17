"""City column from the description of bank transactions.

Public entry point: run(descriptions, cities). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import pandas as pd


def convert_all_text_to_lower(text_list):
    """Convert all text in the list to lower case"""
    return [city.lower() for city in text_list]


def get_last_word(description):
    """Split the description column and get the last word"""
    return description.lower().split()[-1]


def get_city_from_description(description, city_list):
    """Get the city from the description"""
    last_word = get_last_word(description)
    return last_word if last_word in city_list else 'Unknown'


def get_city_from_description_with_fallback(description, city_list):
    """Get the city from the description, with fallback to second last word if first is not found"""
    last_word = get_last_word(description)
    if last_word == 'Unknown':
        second_last_word = description.lower().split()[-2]
        return second_last_word.lower() if second_last_word in city_list else 'Unknown'
    return last_word


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = convert_all_text_to_lower(city_list)
    # split the description column and get the last word
    df['City'] = df['Description'].apply(get_last_word)
    # check if the last word in the description is in the city list
    df['City'] = df['City'].apply(get_city_from_description, args=(city_list,))
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def run(descriptions, cities):
    """Classifies the descriptions. Public entry point of this unit."""
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
