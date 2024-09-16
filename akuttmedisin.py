import pandas as pd

from functions.grouped_descriptive_stat import collect_grouped_counts
from functions.month_day_table import summarize_day_month_counts


def akuttmedisin():
    df = pd.read_csv('dataset/akuttmedisin.csv', sep=";", encoding="utf-8")

    unike_avdelinger = df['LocationName'].unique().tolist()
    for avdeling in unike_avdelinger:
        avd = df[(df["LocationName"] == avdeling)]
        num_individuals = avd['FirstName'].nunique()
        deviation_codes = {"egenmeldinger": "EM", "interne bytter": "IB"}
        for case, code in deviation_codes.items():
            num_obs = avd[avd['DeviationTypeShortName'] == code].shape[0]
            condition_individuals = avd[avd['DeviationTypeShortName'] == 'EM']['FirstName'].nunique()
            summarize_day_month_counts(avd, 'dayName', 'monthName', 'DeviationTypeShortName', code, f'Antall {case} 2023 :  {avdeling}', f"Datasettet er hentet fra visma. I systemet er {case} registrert som avvik med avvikskoden '{code}'. Tallene i koordinatsystemet ovenfor viser antall {case} registrert i løpet av måneden, fordelt på hvilken ukedag tilfellene fant sted. Avdelingen '{avdeling}' hadde totalt {num_individuals} registrerte ansatte. Det funnet {case} for {condition_individuals} ({int(round(condition_individuals/num_individuals, 2)*100)}%) av de ansatte i løpet av 2023. Totalt er det observert {num_obs} avvik med koden '{code}'.", output_filename=f'tabels/akuttmedisin/{case}_{avdeling}.xlsx')
