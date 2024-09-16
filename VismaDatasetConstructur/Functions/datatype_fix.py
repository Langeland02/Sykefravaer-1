import pandas as pd


def fix_datatype(df):
    df['Shiftdate'] = pd.to_datetime(df['Shiftdate'])

    # Remove duplicates, keeping the row with the highest 'PositionSize'
    df = df.sort_values('PositionSize', ascending=True).drop_duplicates(
        subset=['FirstName', 'Shiftdate'],
        keep='first')

    # Sort by FirstName and Shiftdate
    df = df.sort_values(by=['LocationName', 'FirstName', 'Shiftdate'])

    df['FirstName'] = df['FirstName'].str.upper()

    df["PositionSize"] = df["PositionSize"].astype(str)
    df["TemplateShiftLenght"] = df["TemplateShiftLenght"].astype(str)
    # Step 2: Replace commas with dots using .loc
    df.loc[:, "PositionSize"] = df["PositionSize"].str.replace(',', '.')
    df.loc[:, "TemplateShiftLenght"] = df["TemplateShiftLenght"].str.replace(',', '.')
    df["PositionSize"] = df["PositionSize"].astype(float)
    df["TemplateShiftLenght"] = pd.to_numeric(df["TemplateShiftLenght"], errors='coerce')

    # Fill NaN values in specific columns
    df['TemplateShiftStart'] = df['TemplateShiftStart'].fillna('00:01')
    df['TemplateShiftEnd'] = df['TemplateShiftEnd'].fillna('00:01')

    # Replace 0 values in specific columns
    df['TemplateShiftStart'] = df['TemplateShiftStart'].replace(0, '00:01')
    df['TemplateShiftEnd'] = df['TemplateShiftEnd'].replace(0, '00:01')

    # Splitting the column into two columns based on the first space
    df[['LocationCode', 'Location']] = df['LocationName'].str.split(n=1, expand=True)

    df = df.dropna(subset=['FirstName'])


    return df