from functions.gen_workCodes_empty import gen_workCodes
from visma_merge import mergeVisma
import pandas as pd

def preprocessing(years):
    for yr in years:
        gen_workCodes(yr)
        mergeVisma(yr)

def master_merge(years):
    # Loop through the years and read each CSV
    dfs = [pd.read_csv(f"outputDatasets/visma{year}.csv", delimiter=';') for year in years]

    # Merge all DataFrames with an outer join
    merged_df = pd.concat(dfs, axis=0, join='outer')


    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv("outputDatasets/omsorgsboliger.csv", index=False, sep=";", encoding="utf-8-sig")


if __name__ == '__main__':
    preprocessing([1])

    years = [2020, 2021, 2022, 2023]
    preprocessing(years)
    master_merge(years)


