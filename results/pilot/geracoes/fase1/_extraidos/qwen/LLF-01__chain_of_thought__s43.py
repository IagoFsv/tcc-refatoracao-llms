import pandas as pd

def get_last_word(df):
    """Extract the last word from the 'Description' column"""
    return df['Description'].str.lower().str.split().apply(lambda x: x[-1])

def get_second_last_word(df):
    """Extract the second last word from the 'Description' column"""
    return df['Description'].str.lower().str.split().apply(lambda x: x[-2])

def update_city_column(df, city_list):
    """Create a new column called 'City' and populate it with the city of the transaction"""
    # Convert all text in city_list to lower case
    city_list = [city.lower() for city in city_list]
    
    # Get the last word from the description
    df['City'] = get_last_word(df)
    
    # Check if the last word in the description is in the city list
    df['City'] = df['City'].apply(lambda x: x if x in city_list else 'Unknown')
    
    # Check the last 2 words in the description if the city column is unknown
    df['City'] = df.apply(lambda x: x['Description'].split()[-2].lower() if x['City'] == 'Unknown' and x['Description'].split()[-2].lower() in city_list else x['City'], axis=1)
    
    # Make city title case
    df['City'] = df['City'].str.title()
    
    return df

def executar(descricoes, cidades):
    """Classifica as descricoes. Ponto de entrada publico desta unidade."""
    df = pd.DataFrame({"Description": descricoes})
    df = update_city_column(df, cidades)
    return df["City"].tolist()
