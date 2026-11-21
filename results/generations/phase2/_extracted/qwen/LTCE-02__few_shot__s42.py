"""City column from the description of bank transactions.

Public entry point: run(descriptions, cities). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import pandas as pd


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    # split the description column and get the last word
    df['City'] = df['Description'].str.lower().str.split().apply(lambda x: x[-1])
    # check if the last word in the description is in the city list
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    # check the last 2 words in the description if the city column is unknown
    df['City'] = df.apply(lambda x: check_last_two_words(x['Description'], city_list) if x['City'] == 'Unknown' else x['City'], axis=1)
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def check_last_two_words(description, city_list):
    """Check the last two words in the description for a match in the city list."""
    words = description.lower().split()
    if len(words) > 1 and words[-2] in city_list:
        return words[-2]
    return 'Unknown'


def run(descriptions, cities):
    """Classifies the descriptions. Public entry point of this unit."""
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
