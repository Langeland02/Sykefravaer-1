import numpy as np
import pandas as pd


def get_yearsInWork(df):
    # Calculate years in work, making it NaN if any of the dates are missing
    df['yearsInWork'] = df.apply(
        lambda row: round((row['Shiftdate'] - row['RegisteredDate']).days / 365.25, 2)
        if pd.notna(row['Shiftdate']) and pd.notna(row['RegisteredDate'])
        else np.nan,
        axis=1
    )

    return df