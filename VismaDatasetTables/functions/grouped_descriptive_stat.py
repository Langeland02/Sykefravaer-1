import pandas as pd


def collect_grouped_counts(df, groupby_column, column_filters, output_filename='tabels/summary_table.xlsx'):
    """
    This function collects the count of specified values for specified columns of a DataFrame,
    grouped by a specific column, and saves a summary table as an Excel file.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    groupby_column (str): The column name to group by.
    column_filters (list of tuples): A list where each tuple contains a column name and a list of specific values to filter by.
    output_filename (str): The filename for the output Excel file.

    Returns:
    None
    """
    if groupby_column not in df.columns:
        raise ValueError(f"Groupby column '{groupby_column}' not found in the DataFrame.")

    for column, _ in column_filters:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame.")

    # Construct header names
    header_names = ['Group'] + [f'{k} is {v}' for k, v in column_filters]

    summary_data = []
    group_values = df[groupby_column].unique().tolist()

    # Loop through each group value
    for group in group_values:
        grouped_data = df[df[groupby_column] == group]
        row = [group]

        # Loop through each column and filter values
        for column, values in column_filters:
            filtered_data = grouped_data[grouped_data[column].isin(values)]
            filtered_count = len(filtered_data)
            row.append(filtered_count)

        summary_data.append(row)

    # Create DataFrame for summary data
    summary_df = pd.DataFrame(summary_data, columns=header_names)

    # Save the summary DataFrame to an Excel file
    summary_df.to_excel(output_filename, index=False)
    print(f"Summary table saved to {output_filename}")
