import pandas as pd

from functions.actualWork import check_columns
from functions.clock_to_timecategory import clock_to_timecategory
from functions.count_workers import count_categorical_exclusions
from functions.datatype_fix import fix_datatype
from functions.fill_rows import fill_rows
from functions.gen_workCodes_empty import gen_workCodes
from functions.getAge import get_age
from functions.get_day_characteristics import get_day_characteristics
from functions.process_interntBytte import process_IB_comments
from functions.work_code import get_work_codes
from functions.years_worked import get_yearsInWork


def mergeVisma(årstall):



    # Laster inn grunnturnus
    deviationTurnus = pd.read_csv(f'originalDatasets/Deviation{årstall}.csv', sep=";", encoding="utf-8")
    grunnTurnus = pd.read_csv(f'originalDatasets/ResursDel{årstall}.csv', sep=";", encoding="utf-8")


    # Convert 'Shiftdate', 'BirthDate', 'RegisteredDate' to datetime
    grunnTurnus['Shiftdate'] = pd.to_datetime(grunnTurnus['Shiftdate'])
    grunnTurnus['BirthDate'] = pd.to_datetime(grunnTurnus['BirthDate'])
    grunnTurnus['RegisteredDate'] = pd.to_datetime(grunnTurnus['RegisteredDate'])

    # Sort the DataFrame by entity and time
    grunnTurnus = grunnTurnus.sort_values(by=['LocationName', 'FirstName', 'Shiftdate'])

    # Assign new column based on the dictionary
    grunnTurnus = get_work_codes(grunnTurnus, årstall)

    # Identify all duplicates
    duplicates_first = grunnTurnus.duplicated(subset=['FirstName', 'Shiftdate'], keep='first')
    duplicates_subsequent = grunnTurnus.duplicated(subset=['FirstName', 'Shiftdate'], keep=False)
    # Combine both to get all duplicates
    all_duplicates = duplicates_first | duplicates_subsequent
    # Filter out all duplicates
    duplicates_df = grunnTurnus[all_duplicates]
    duplicates_df.to_csv(f'outputDatasets/duplicates_{årstall}.csv', sep=";", encoding="utf-8")

    # Assuming 'df' is your DataFrame and 'PositionSize' is the column name
    grunnTurnus['PositionSize'] = grunnTurnus['PositionSize'].str.replace(',', '.').astype(float)
    # Remove duplicates, keeping the row with the highest 'PositionSize'
    grunnTurnus = grunnTurnus.sort_values('PositionSize', ascending=False).drop_duplicates(subset=['FirstName', 'Shiftdate'],
                                                                         keep='first')

    # Sort by FirstName and Shiftdate
    grunnTurnus = grunnTurnus.sort_values(by=['LocationName', 'FirstName', 'Shiftdate'])

    # Drop the specified columns
    grunnTurnus = grunnTurnus.drop(columns=['BaseShiftCode', 'BaseShiftLenght', 'BaseShiftStart', 'BaseShiftEnd'])

    grunnTurnus.fillna(0, inplace=True)  # fill with zeros



    # Convert 'Shiftdate' to datetime
    deviationTurnus['DeviationDate'] = pd.to_datetime(deviationTurnus['DeviationDate'], errors='coerce')

    # Rename the columns in df1 to match df2 for merging
    deviationTurnus = deviationTurnus.rename(columns={'DeviationDate': 'Shiftdate'})

    # Convert 'BirthDate' to datetime
    deviationTurnus['BirthDate'] = pd.to_datetime(deviationTurnus['BirthDate'], errors='coerce')


    # Convert 'BirthDate' to datetime
    deviationTurnus['RegisteredDate'] = pd.to_datetime(deviationTurnus['RegisteredDate'], errors='coerce')

    ##########################################################################################
    ##########################################################################################
    ##########################################################################################

    # Ensure 'Shiftdate' is in datetime64[ns] format in both DataFrames
    grunnTurnus['Shiftdate'] = pd.to_datetime(grunnTurnus['Shiftdate'])
    deviationTurnus['Shiftdate'] = pd.to_datetime(deviationTurnus['Shiftdate'])

    # Perform the merge
    merged_df = pd.merge(grunnTurnus, deviationTurnus[['FirstName', 'Shiftdate', 'LocationName', 'DeviationTypeShortName', 'DeviationTypeName', 'DeviationText']], on=['LocationName', 'FirstName', 'Shiftdate'], how='outer')

    merged_df = process_IB_comments(merged_df, 'Shiftdate', 'FirstName', 'DeviationTypeShortName', 'DeviationText')

    # Finner radene der det har fåregått interne bytter, og forsøker å finne vakttypen, sletter rader med IB dersom faktisk vakt er lokalisert
    merged_df = check_columns(merged_df, 'change', 'DeviationTypeShortName', 'TemplateCode', årstall)

    merged_df = fix_datatype(merged_df)

    merged_df = clock_to_timecategory(merged_df)

    merged_df = count_categorical_exclusions(merged_df, 'Shiftdate', 'actualCode', 'totalCountedWorkers')

    merged_df = fill_rows(merged_df)

    merged_df = get_age(merged_df)

    merged_df = get_yearsInWork(merged_df)

    merged_df = get_day_characteristics(merged_df)

    columns_to_drop = [
    "DocumetName", "DocumentID", "TemplateCodeName", "TemplateShiftLenght",
    "TemplateShiftStart", "TemplateShiftEnd", "BaselateCodeName", "TypeName", "Type",
    "DeviationTypeName", "DeviationText", "NewDate", "Phrase", "change",
    "LocationCode", "Location",
    "dagvakter", "mellomvakter", "kveldsvakter", "nattvakter", "langvakter",
    "vikarvakter", "udefinerte vakter", "totalCountedWorkers"


]
    # Drop columns only if they exist in the DataFrame
    merged_df = merged_df.drop(columns=[col for col in columns_to_drop if col in merged_df.columns])



    merged_df.to_csv(f'outputDatasets/visma{årstall}.csv', sep=";", encoding="utf-8-sig")







