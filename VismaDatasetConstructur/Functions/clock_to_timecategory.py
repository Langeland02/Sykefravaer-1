import pandas as pd
from datetime import datetime, timedelta

def round_to_nearest_quarter_hour(dt):
    # Round the datetime object to the nearest quarter-hour
    new_minute = (dt.minute // 15) * 15
    if dt.minute % 15 >= 7.5:
        new_minute += 15
    if new_minute == 60:
        dt = dt + timedelta(hours=1)
        new_minute = 0
    return dt.replace(minute=new_minute, second=0, microsecond=0)
def clock_to_timecategory(df):
    fmt = '%H:%M'

    shift_variables = []
    for index, row in df.iterrows():
        start = str(row['TemplateShiftStart'])
        end = str(row['TemplateShiftEnd'])

        # Ensure the values are strings and handle potential errors
        try:
            start_time = datetime.strptime(start, fmt)
            end_time = datetime.strptime(end, fmt)

            # Round to the nearest quarter-hour
            start_time = round_to_nearest_quarter_hour(start_time)
            end_time = round_to_nearest_quarter_hour(end_time)

            if end_time == start_time:
                # Special case for 24-hour shifts
                shift_variable = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}-24h"
            else:
                if end_time < start_time:
                    end_time += timedelta(days=1)  # handle overnight shifts
                duration = end_time - start_time
                hours = duration.seconds // 3600
                shift_variable = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}-{hours}h"
        except ValueError:
            shift_variable = ""  # Add a blank string in case of an error

        shift_variables.append(shift_variable)

    df['ShiftVariable'] = shift_variables

    # Adding the new column 'ShiftLength_Hours' only when actualCode is A, D, M, L
    df['ShiftLength_Hours'] = df.apply(
        lambda row: row['TemplateShiftLenght'] if row['actualCode'] in ['A', 'D', 'M', 'L', 'N'] else None, axis=1)

    return df