# List of people over 80 you want to include
    include_list = ('INGRIDHELENELÆRLING','DIANA','BIRK','HELENEMBAW','EMILIE','KRISTIN','NATHANIEL',
                    'NELLIELÆRLING(100%)','ØVENSENLIV','LISBETH100%','VARGASTABATHACECILIAROBOTHAM',
                    'HELGSHARRONTORSØE','CELINAOLÆRLING','LAUVNESINGRID','JUDITHHKRISTIANSEN',
                    'EIKÅSJOHANNASIGRIDUR','EIKÅSJOHANNASIGRIDUR','PATRICKALANMFY','SIRENTORKILDSEN',
                    'CATHRINESVENDESEN','LINNIVALO','LANGENESRANDI','VAKANTANETTE','LÆRLINGTAMAR',
                    'LÆRLINGDANIEL','AWINLÆRLING','JEMIMALÆRLING','NARGESLÆRLING','NATALIELÆRLING',
                    'KARINLOFTET','MJÅLANDAUDRANDI','TORRESPEDROAREVALO','NINA-LÆRLING','IRENE',
                    'SÆTERDALBIRGITIRENE','BYTANNKRISTIN80%','MIRJAM AKSELSEN // SKOG','*SOMKID BUNPAN HELGA',
                    'IDA HAGELAND','# ALEMU T.YENEAYEHU','# REGINE ROSKIFTE# KAMILLA KOFOED','# STINE SAMULELSEN',
                    'ANDREA 20% 5/2-20','§ ELSE MARIE §','DIANE','ANDREA KVELD 16,37',
                    '# NY JADRANKA 02.01.22-22.05-22','# NY JADRANKA 24.10.22-03.01.23','LÆRLING SAMRAWITH (RODA)',
                    'MARIJA- ORIGINAL','MARTHA 2 HELG','§ SANDRA SIMONSEN §','INGER MARIE WITTEVEEN',
                    'ÅSE THOMASSEN- ØKE 100 %','LÆRLING WASI N.MUKAZ','LÆRLING EMILIE','LÆRLING TERJE','DIANE',
                    'KAREN ( LÆRLING)','MARTINE BJØRNDAL MOTRØEN','ADEM SOMMER','EMILIE VALERIA ODA DE SENA',
                    'LÆRLING JAN CHRISTIAN','LÆRLING LEIF','BORGHILD VESTØL','ELIN HELG MIDLERTIDIG',
                    'KAHSAY LÆRLING','INA MARIELL SOMMER','BETTY','ELISE NATT','HAZBIJE','HANS ALFRED FOSSELIE',
                    'LARS','MICHELLE SOMMER 80%','ELISE','LIV IRENE 20%','AMIN','ANDRE','ARNT ERIK ROGNSVÅG',
                    'HANNA SIKORA','KARINA','KENNETH','MARTINE BJØRNDAL MOTRØEN','AMIN',
                    'NELLIE MARIE HAGEN- LÆRLING', 'KATARINA VEILEDER','CECILIE BROCHMANN','LÆRLING HAIMANOT',
                    'LINN MARI VIKAR','INKAMILLA 20% FRA 15.09.23','GER LISE 50 %','LANGENES MAI BRITT',
                    'LANGENES RUZA','ARBEIDSUTPRØVING KARINA','LÆRLING FREDRIK HILLE','ELISE FAST STILLING',
                    'MARIANNE','ADEM- LÆRLING','NELLIE MARIE HAGEN- LÆRLING, KATARINA VEILEDER',
                    'MARIANA FAST HELG','MELEK VIKARIAT HELG') # Add the names you want to include


    # Identify and save the names of people over 80 to an Excel file
    excluded_people = df[(df['Age'] > 80) & (~df['FirstName'].isin(include_list))][
        ['FirstName', 'Age', 'PositionSize', 'Shiftdate', 'year', 'DeviationTypeShortName','LocationName']]
    excluded_people.to_excel('excluded_people_over_80ny.xlsx', index=False)
    print("Excel file 'excluded_people_over_80ny.xlsx' created with the names of people over 80.")

    # Save all rows that do not have age specified to an Excel file
    no_age_specified = df[df['Age'].isna()][['FirstName', 'Age', 'PositionSize', 'Shiftdate', 'year', 'DeviationTypeShortName','LocationName']]
    no_age_specified.to_excel('no_age_specified.xlsx', index=False)
    print("Excel file 'no_age_specified.xlsx' created with the rows that do not have age specified.")

    # Exclude all rows where age is over 80 and not in the include_list
    df = df[(df['Age'] <= 80)| df['FirstName'].isin(include_list)][['Unnamed: 0','LocationName','FirstName','BirthDate','GenderID',
                                                                    'SalaryPerYear','RegisteredDate','PositionSize','WorkPositionID',
                                                                    'JobStatus','jobTitle','jobCode','Shiftdate','TemplateCode',
                                                                    'DeviationTypeShortName','actualCode','actualCodeName','ShiftVariable',
                                                                    'ShiftLength_Hours','Age','AgeCategory','yearsInWork','dayName',
                                                                    'monthName','year','holidayName']]
    # Lagre til en CSV-fil
    df.to_csv('filtered_data.csv', sep=";", encoding="utf-8-sig")
