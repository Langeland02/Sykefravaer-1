

def fill_rows(df):
    # Fill missing values with fixed data
    fixed_columns = ['BirthDate', 'SalaryPerYear',
                     'RegisteredDate', 'PositionSize', 'WorkPositionID', 'JobStatus', 'jobTitle', 'jobCode',
                     'DocumetName', 'DocumentID', 'Location']

    # For each fixed column, fill the missing values with the first non-null value in the group
    for col in fixed_columns:
        df[col] = df.groupby('FirstName')[col].transform(lambda x: x.ffill().bfill())

    try:
        df['GenderID'] = df.groupby('FirstName')['GenderID'].transform(lambda x: x.ffill().bfill())
    except:
        pass


    return df
