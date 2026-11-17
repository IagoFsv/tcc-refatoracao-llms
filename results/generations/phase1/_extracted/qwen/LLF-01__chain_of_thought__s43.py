"""City column from the description of bank transactions.

Public entry point: run(descriptions, cities). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import pandas as pd


def extract_last_word(description):
    """Extract the last word from the description."""
    return description.lower().split()[-1]


def check_city_in_list(city, city_list):
    """Check if the city is in the city list."""
    return city in city_list


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    
    # Extract the last word from the description
    df['City'] = df['Description'].apply(extract_last_word)
    
    # Check if the last word in the description is in the city list
    df['City'] = df['City'].apply(lambda x: x if check_city_in_list(x, city_list) else 'Unknown')
    
    # Check the last 2 words in the description if the city column is unknown
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and check_city_in_list(x['Description'].split()[-2].lower(), city_list) else x['City'], axis=1)
    
    # Make city title case
    df['City'] = df['City'].str.title()
    return df


def run(descriptions, cities):
    """Classifies the descriptions. Public entry point of this unit."""
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
