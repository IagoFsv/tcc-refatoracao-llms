"""City column from the description of bank transactions.

Public entry point: run(descriptions, cities). Do not change its name or signature; the
rest of the file may be freely reorganized.
"""

import pandas as pd


def update_city_column(df, city_list):
    """Create a new column called city and populate it with the city of the transaction"""
    # convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    
    def get_city_from_description(description):
        words = description.lower().split()
        if words[-1] in city_list:
            return words[-1]
        if len(words) > 1 and words[-2] in city_list:
            return words[-2]
        return 'Unknown'
    
    df['City'] = df['Description'].apply(get_city_from_description)
    # make city title case
    df['City'] = df['City'].str.title()
    return df


def run(descriptions, cities):
    """Classifies the descriptions. Public entry point of this unit."""
    df = pd.DataFrame({"Description": descriptions})
    df = update_city_column(df, cities)
    return df["City"].tolist()
