# Function to determine holidays
def determine_holiday(date):
    if date.month == 12 and 23 <= date.day <= 26:
        return 'Jul'
    elif (date.month == 12 and date.day == 31) or (date.month == 1 and date.day == 1):
        return 'Nyttår'
    elif date.month == 4 and 6 <= date.day <= 10:  # Skjærtorsdag to 2. påskedag in 2023
        return 'Påske'
    elif date.month == 5 and date.day == 1:
        return 'Arbeiderenes dag'
    elif date.month == 5 and date.day == 17:
        return '17. mai'
    elif date.month == 5 and date.day == 18:  # Kristi himmelfart in 2023
        return 'Kristi himmelfart'
    elif date.month == 5 and 27 <= date.day <= 29:  # Pinse in 2023
        return 'Pinse'
    elif date.month == 2 and 22 <= date.day <= 26:  # Example week for Vinterferie
        return 'Vinterferie'
    elif date.month == 7 and 10 <= date.day <= 31:  # Example period for Fellesferie
        return 'Fellesferie'
    elif date.month == 10 and 2 <= date.day <= 6:  # Example week for Høstferie
        return 'Høstferie'
    else:
        return 'Normal'