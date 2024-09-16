import json

# Function to map TemplateCode to TypeName or Type based on index
def map_template_code(row, index, code_dict):
    location_dict = code_dict.get(row['LocationName'], {})
    return location_dict.get(row['TemplateCode'], ["", ""])[index]

def get_work_codes(df, årstall):
    code_dict = json.load(open(f'helperDatasets/workCodes_{årstall}.json', encoding='utf-8'))
    df['TypeName'] = df.apply(lambda row: map_template_code(row, 1, code_dict), axis=1)
    df['Type'] = df.apply(lambda row: map_template_code(row, 0, code_dict), axis=1)
    return df