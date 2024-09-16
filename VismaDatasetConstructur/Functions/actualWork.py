import json

import pandas as pd


def check_columns(df, change_col, deviations_col, original_col, årstall):
    """
    Iterates through the DataFrame row by row, checks specified columns, stores their values in a list, and creates a new column.

    Parameters:
    df (pd.DataFrame): The DataFrame to iterate through.
    change_col (str): The name of the column representing changes.
    deviations_col (str): The name of the column representing deviations.
    original_col (str): The name of the column representing original values.
    new_col_name (str): The name of the new column to be added.

    Returns:
    pd.DataFrame: The updated DataFrame with the new column.
    """

    new_column_data = []
    code_dict = json.load(open(f'helperDatasets/workCodes_{årstall}.json', encoding='utf-8'))

    for idx, row in df.iterrows():
        change_value = row[change_col]
        deviations_value = row[deviations_col]
        original_value = row[original_col]
        location = row['LocationName']

        if pd.notna(deviations_value):
            try:
                new_value = code_dict[location][str(deviations_value)][0]
            except:
                new_value = "U"  # Ukategorisert
        else:
            try:
                new_value = code_dict[location][str(original_value)][0]
            except:
                new_value = "U" #Ukategorisert



        new_column_data.append(new_value)

    df['actualCode'] = new_column_data
    # Mapping of categories to their respective names
    category_mapping = {
        'F': 'Ferie & avspasering',
        'X': 'Jobber i annen avdeling',
        'A': 'Aftenvakt',
        'W': 'Ukategorisert vakt',
        'N': 'Nattvakt',
        'D': 'Dagvakt',
        'S': 'Syk',
        'V': 'Vikarvakt',
        'L': 'Langvakt',
        'P': 'Permisjon',
        'M': 'Mellomvakt',
        'B': 'Barnrelatert',
        'O': 'Fravær',
        'K': 'Kontor',
        'IB': 'Internt bytte',
        'OT': 'Overtid'
    }

    # Replace the category letters in 'actualCode' column with their respective names
    df['actualCodeName'] = df['actualCode'].map(category_mapping)
    return df