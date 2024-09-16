from datetime import date

def determine_holiday(date):
    if date.month == 12 and 23 <= date.day <= 26:
        return 'Jul'
    elif (date.month == 12 and date.day == 31) or (date.month == 1 and date.day == 1):
        return 'Nyttår'
    elif date.year in [2020, 2021, 2022, 2023, 2024]:
        if date.year == 2020:
            if date.month == 4 and 9 <= date.day <= 13:  # Skjærtorsdag to 2. påskedag in 2020
                return 'Påske'
            elif date.month == 5 and date.day == 1:
                return 'Arbeiderenes dag'
            elif date.month == 5 and date.day == 17:
                return '17. mai'
            elif date.month == 5 and date.day == 21:  # Kristi himmelfart in 2020
                return 'Kristi himmelfart'
            elif date.month == 5 and 30 <= date.day <= 31:  # Pinse in 2020
                return 'Pinse'
        elif date.year == 2021:
            if date.month == 4 and 1 <= date.day <= 5:  # Skjærtorsdag to 2. påskedag in 2021
                return 'Påske'
            elif date.month == 5 and date.day == 1:
                return 'Arbeiderenes dag'
            elif date.month == 5 and date.day == 17:
                return '17. mai'
            elif date.month == 5 and date.day == 13:  # Kristi himmelfart in 2021
                return 'Kristi himmelfart'
            elif date.month == 5 and 22 <= date.day <= 24:  # Pinse in 2021
                return 'Pinse'
        elif date.year == 2022:
            if date.month == 4 and 14 <= date.day <= 18:  # Skjærtorsdag to 2. påskedag in 2022
                return 'Påske'
            elif date.month == 5 and date.day == 1:
                return 'Arbeiderenes dag'
            elif date.month == 5 and date.day == 17:
                return '17. mai'
            elif date.month == 5 and date.day == 26:  # Kristi himmelfart in 2022
                return 'Kristi himmelfart'
            elif date.month == 6 and 4 <= date.day <= 6:  # Pinse in 2022
                return 'Pinse'
        elif date.year == 2023:
            if date.month == 4 and 6 <= date.day <= 10:  # Skjærtorsdag to 2. påskedag in 2023
                return 'Påske'
            elif date.month == 5 and date.day == 1:
                return 'Arbeiderenes dag'
            elif date.month == 5 and date.day == 17:
                return '17. mai'
            elif date.month == 5 and date.day == 18:  # Kristi himmelfart in 2023
                return 'Kristi himmelfart'
            elif date.month == 5 and 27 <= date.day <= 29:  # Pinse in 2023
                return 'Pinse'
        elif date.year == 2024:
            if date.month == 3 and 28 <= date.day <= 31:  # Skjærtorsdag to 1. påskedag in 2024
                return 'Påske'
            elif date.month == 4 and date.day == 1:  # 2. påskedag in 2024
                return 'Påske'
            elif date.month == 5 and date.day == 1:
                return 'Arbeiderenes dag'
            elif date.month == 5 and date.day == 17:
                return '17. mai'
            elif date.month == 5 and date.day == 9:  # Kristi himmelfart in 2024
                return 'Kristi himmelfart'
            elif date.month == 5 and 18 <= date.day <= 20:  # Pinse in 2024
                return 'Pinse'


def get_day_characteristics(df):
    # Create mappings for day and month names in Norwegian
    day_name_map = {
        'Monday': 'Mandag', 'Tuesday': 'Tirsdag', 'Wednesday': 'Onsdag', 'Thursday': 'Torsdag',
        'Friday': 'Fredag', 'Saturday': 'Lørdag', 'Sunday': 'Søndag'
    }

    month_name_map = {
        'January': 'Januar', 'February': 'Februar', 'March': 'Mars', 'April': 'April',
        'May': 'Mai', 'June': 'Juni', 'July': 'Juli', 'August': 'August',
        'September': 'September', 'October': 'Oktober', 'November': 'November', 'December': 'Desember'
    }

    # Extract day and month names in English and map to Norwegian
    df['dayName'] = df['Shiftdate'].dt.day_name().map(day_name_map)
    df['monthName'] = df['Shiftdate'].dt.month_name().map(month_name_map)
    df['year'] = df['Shiftdate'].dt.year
    # Apply the function to determine the holiday for each date

    df['holidayName'] = df['Shiftdate'].apply(determine_holiday)

    return df