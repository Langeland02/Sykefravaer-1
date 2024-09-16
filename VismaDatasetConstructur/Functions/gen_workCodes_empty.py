import json

import pandas as pd


def gen_workCodes(årstall):
    # Laster inn grunnturnus
    df_deviations = pd.read_csv(f'originalDatasets/Deviation{årstall}.csv', sep=";", encoding="utf-8")
    df = pd.read_csv(f'originalDatasets/ResursDel{årstall}.csv', sep=";", encoding="utf-8")
    df_helper = pd.read_json('helperDatasets/workCodes_helper.json', encoding="utf-8", typ='series').to_frame('value')
    print(df_helper)

    unique_values = df['LocationName'].unique()

    _dict = {}

    for location in unique_values:
        # Filter the DataFrame
        sub_df = df[df['LocationName'] == location]
        sub_df_deviations = df_deviations[df_deviations['LocationName'] == location]

        unique_shifts = [str(item) for item in list(sub_df['TemplateCode'].unique())]
        unique_deviations = [str(item) for item in list(sub_df_deviations['DeviationTypeShortName'].unique())]

        unique_deviation_names = [str(item) for item in list(sub_df_deviations['DeviationTypeName'].unique())]

        all_codes = unique_shifts + unique_deviations
        all_names = ["" for i in unique_shifts] + unique_deviation_names



        _dict[location] = {all_codes[i]: [df_helper.loc[all_codes[i], 'value'] if all_codes[i] in df_helper.index else "", all_names[i], ""] for i in range(len(all_codes))}


        # Step 2: Sort the dictionary by keys
        _dict[location] = {k: _dict[location][k] for k in sorted(_dict[location])}

    unique_values =  [list(v.keys()) for v in _dict.values()]
    unique_strings = sorted(list(set(string for sublist in unique_values for string in sublist)))
    helper_dict = {k:"" for k in unique_strings}

    print(str(helper_dict).replace("'", '"').replace('""', '"U"'))

    # Open a file for writing
    with open(f'helperDatasets/workCodes_{årstall}.json', 'w', encoding='utf-8') as json_file:
        # Write the dictionary to the file in JSON format
        json.dump(_dict, json_file)




