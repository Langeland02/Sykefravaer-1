import pandas as pd

from functions.grouped_descriptive_stat import collect_grouped_counts
from functions.month_day_table import summarize_day_month_counts


def omsorgsboliger():
    df = pd.read_csv('dataset/omsorgsboliger.csv', sep=";", encoding="utf-8")


    # Ekskluder individer med alder over 70
    df = df[df['Age'] <= 70]

    years = [2020, 2021, 2022, 2023]
    column_filters = [
        ('actualCode', ['D']),
        ('actualCode', ['N']),
        ('actualCode', ['A', 'D', 'M', 'N', 'L']),
        ('DeviationTypeShortName', ['EM']),
        ('actualCode', ['B']),
        ('actualCode', ['M']),
        ('actualCode', ['A']),
        ('actualCode', ['L']),
        ('actualCode', ['IB'])
    ]
    collect_grouped_counts(df, 'LocationName', column_filters, output_filename='tabels/summary_table.xlsx')
    unike_avdelinger = df['LocationName'].unique().tolist()
    for year in years:
        for avdeling in unike_avdelinger:
            avd = df[(df["LocationName"] == avdeling) & (df["year"] == year)]
            num_individuals = avd['FirstName'].nunique()
            deviation_codes = {"egenmeldinger": "EM", 'Sykemeldinger (over 16 dager)': 'SO',  'Sykemeldinger (under 17 dager)': 'SU', 'Overtid': 'OT', 'Ekstravakt': 'EV'}
            for case, code in deviation_codes.items():
                num_obs = avd[avd['DeviationTypeShortName'] == code].shape[0]
                condition_individuals = avd[avd['DeviationTypeShortName'] == 'EM']['FirstName'].nunique()
                if num_individuals > 0:
                    summarize_day_month_counts(avd, 'dayName', 'monthName', 'DeviationTypeShortName', code,
                                           f'Antall {case} {year} :  {avdeling}',
                                           f"Datasettet er hentet fra visma. I systemet er {case} registrert som avvik med avvikskoden '{code}'. Tallene i koordinatsystemet ovenfor viser antall {case} registrert i løpet av måneden, fordelt på hvilken ukedag tilfellene fant sted. Avdelingen '{avdeling}' hadde totalt {num_individuals} registrerte ansatte. Det funnet {case} for {condition_individuals} ({int(round(condition_individuals / num_individuals, 2) * 100)}%) av de ansatte i løpet av 2023. Totalt er det observert {num_obs} avvik med koden '{code}'.",
                                           output_filename=f'tabels/omsorgsboliger/{case}_{avdeling}_{year}_ny.xlsx')
                else:
                    summarize_day_month_counts(avd, 'dayName', 'monthName', 'DeviationTypeShortName', code,
                                               f'Antall {case} {year} :  {avdeling}',
                                               f"Datasettet er hentet fra visma. I systemet er {case} registrert som avvik med avvikskoden '{code}'. Tallene i koordinatsystemet ovenfor viser antall {case} registrert i løpet av måneden, fordelt på hvilken ukedag tilfellene fant sted. Avdelingen '{avdeling}' hadde totalt {num_individuals} registrerte ansatte. Det funnet {case} for {condition_individuals} av de ansatte i løpet av 2023. Totalt er det observert {num_obs} avvik med koden '{code}'.",
                                               output_filename=f'tabels/omsorgsboliger/{case}_{avdeling}_{year}ny.xlsx')
