
def count_categorical_exclusions(df, date_col, categorical_col, new_col_name):
    """
    Counts occurrences of a categorical column in a panel dataset, excluding values "S," "X," and "F."
    Adds the result as a new column in the original dataset.

    Parameters:
    df (pd.DataFrame): The panel dataset.
    date_col (str): The name of the column representing the date dimension.
    individual_col (str): The name of the column representing individuals.
    categorical_col (str): The name of the categorical column to count.
    new_col_name (str): The name of the new column to be added.

    Returns:
    pd.DataFrame: The updated DataFrame with the new column.
    """
    # Initialize a dictionary to store counts by date
    counts_by_date = {}
    counts_dagvakt = {}
    counts_mellomvakt = {}
    counts_kveldsvakt = {}
    counts_nattvakt = {}
    counts_langvakt = {}
    counts_vikar = {}
    counts_udefinert_vakt = {}


    # Get unique dates
    unique_dates = df[date_col].unique()

    # Loop over each unique date
    for date in unique_dates:
        # Filter the DataFrame for the current date
        date_df = df[df[date_col] == date]


        # Count individuals with categorical column equal to
        count_d = date_df[date_df[categorical_col] == 'D'].shape[0]
        count_m = date_df[date_df[categorical_col] == 'M'].shape[0]
        count_a = date_df[date_df[categorical_col] == 'A'].shape[0]
        count_n = date_df[date_df[categorical_col] == 'N'].shape[0]
        count_l = date_df[date_df[categorical_col] == 'L'].shape[0]
        count_v = date_df[date_df[categorical_col] == 'V'].shape[0]
        count_w = date_df[date_df[categorical_col] == 'W'].shape[0]

        count_exclusions = count_d+count_m+count_a+count_n+count_l+count_v+count_w


        # Store the count for the current date
        counts_by_date[date] = count_exclusions
        counts_dagvakt[date] = count_d
        counts_mellomvakt[date] = count_m
        counts_kveldsvakt[date] = count_a
        counts_nattvakt[date] = count_n
        counts_langvakt[date] = count_l
        counts_vikar[date] = count_v
        counts_udefinert_vakt[date] = count_w


    # Map the counts to the original DataFrame
    df['dagvakter'] = df[date_col].map(counts_dagvakt)
    df['mellomvakter'] = df[date_col].map(counts_mellomvakt)
    df['kveldsvakter'] = df[date_col].map(counts_kveldsvakt)
    df['nattvakter'] = df[date_col].map(counts_nattvakt)
    df['langvakter'] = df[date_col].map(counts_langvakt)
    df['vikarvakter'] = df[date_col].map(counts_vikar)
    df['udefinerte vakter'] = df[date_col].map(counts_udefinert_vakt)
    df[new_col_name] = df[date_col].map(counts_by_date)

    return df

