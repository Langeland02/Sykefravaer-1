import re
from datetime import datetime

import pandas as pd


def process_IB_comments(df, time_col, individual_col, status_col, comment_col):
    """
    Processes the DataFrame to check for 'IB' status and extracts dates and phrases from comments.

    Parameters:
    df (pd.DataFrame): The panel dataset.
    time_col (str): The name of the column representing the time dimension.
    individual_col (str): The name of the column representing individuals.
    status_col (str): The name of the column to check for the value 'IB'.
    comment_col (str): The name of the column containing comments.

    Returns:
    pd.DataFrame: Updated DataFrame with new rows added based on the comments.
    """

    # Initialize new columns
    df['NewDate'] = pd.NaT
    df['Phrase'] = ''
    df['change'] = ''

    new_rows = []
    indices_to_drop = []

    # Iterate through the DataFrame
    for idx, row in df.iterrows():
        if row[status_col] == 'IB':
            base_date = pd.to_datetime(row[time_col])
            comment = row[comment_col]
            extracted_info = extract_info_from_comment(comment, base_date)
            if extracted_info['date']:
                new_row = row.copy()
                new_row[time_col] = extracted_info['date']
                new_row['NewDate'] = extracted_info['date']
                new_row['Phrase'] = extracted_info['phrase'] if extracted_info['phrase'] else 'No specific phrase'
                new_row['change'] = extracted_info['change'] if extracted_info['change'] else 'N/A'
                new_rows.append(new_row)
                if extracted_info['change'] != 'F':
                    indices_to_drop.append(idx)

    # Drop the old rows from the DataFrame that do not have Letter 'F'
    df = df.drop(indices_to_drop).reset_index(drop=True)

    # Append new rows to the updated DataFrame
    new_df = pd.DataFrame(new_rows)
    df = pd.concat([df, new_df], ignore_index=True)

    return df

def extract_info_from_comment(comment, base_date):
    """
    Extracts the date and specific phrases from the comment string.
    The date is assumed to be in the format 'dd.mm' or 'dd.mm.'.
    Also extracts phrases like "byttet mot fri," "byttet til," "byttet mot N," "byttet med (person)".
    The year from the base_date is used to construct the full date.

    Parameters:
    comment (str): The comment string.
    base_date (datetime): The base date to extract the year from.

    Returns:
    dict: Extracted information with date, phrase, and a corresponding letter.
    """
    info = {'date': None, 'phrase': None, 'change': None}
    year = base_date.year

    if pd.notna(comment):
        comment = str(comment).lower()
        date_pattern = re.compile(r'\b(\d{1,2}\.\d{1,2})\b')
        dates = date_pattern.findall(comment)
        if dates:
            date_str = dates[-1]
            try:
                info['date'] = datetime.strptime(f'{date_str}.{year}', '%d.%m.%Y').strftime('%Y-%m-%d')
            except ValueError:
                pass

        # Phrase patterns and corresponding letters
        phrase_patterns = {
            'byttet mot fri': 'F',
            'byttet til': 'W',
            'flyttet til': 'W',
            'byttet mot n': 'N',
            'byttet mot': 'W',
            'mot fri': 'F',
            'fri mot': 'W',
            'byttet med': 'W',
            'mot': 'W',
            'jobber mot fri': 'F',
            'jobber': 'W',
        }

        for pattern, letter in phrase_patterns.items():
            if pattern in comment:
                info['phrase'] = pattern
                info['change'] = letter
                return info


    return {'date': None}

