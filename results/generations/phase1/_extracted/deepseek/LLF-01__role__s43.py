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
    # check the last 2 words in the descirption if the city columns is unknown. Compare the 2 words to the city list for a match. If there is a match, add the city name to the city column
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and x['Description'].split()[-2].lower() in city_list else x['City'], axis=1)
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def run(descriptions, cities):
    """Classifies the descriptions. Public entry point of this unit."""
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
