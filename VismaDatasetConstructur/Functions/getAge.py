import numpy as np
import pandas as pd


def categorize_by_age(df):
    # Define age categories
    age_bins = [0, 25, 30, 40, 50, 60, 70, 80, float('inf')]
    age_labels = ['yngre enn 25 år', '25 til 30', '30-årene', '40-årene', '50-årene', '60-årene',
                  '70-årene', 'annet']

    # Initialize a dictionary to store the initial age category of each individual
    initial_age_categories = {}

    # Loop through each unique individual in the FirstName column
    for name in df['FirstName'].unique():

        # Get the first occurrence of the individual in the DataFrame
        first_occurrence = df[df['FirstName'] == name].iloc[0]

        # Determine the initial age category for the individual
        initial_age_category = pd.cut([first_occurrence['Age']], bins=age_bins, labels=age_labels, right=False)[0]

        # Store the initial age category in the dictionary
        initial_age_categories[name] = initial_age_category

    # Create a new column in the DataFrame for the age category
    df['AgeCategory'] = df['FirstName'].map(initial_age_categories)

    return df

def get_age(df):
    # Calculating the age
    df['Age'] = df.apply(lambda row: row['Shiftdate'].year - row['BirthDate'].year if pd.notnull(row['Shiftdate']) and pd.notnull(row['BirthDate']) else np.nan, axis=1)

    df = categorize_by_age(df)

    # Exclude individuals over the age of 70
    df = df[df['Age'] <= 70]

    return df