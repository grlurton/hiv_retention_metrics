import os
#from dotenv import load_dotenv, find_dotenv
import src.data.get_kenya as get_kenya
import src.data.get_haiti as get_haiti

kenya = False
haiti = True

# Loading Kenya
if kenya :
    kenya_1_url = os.environ.get("kenya_1_url")
    kenya_2_visits_url = os.environ.get("kenya_2_visits_url")
    kenya_2_patients_url = os.environ.get("kenya_2_patients_url")
    kenya_3_visits_url = os.environ.get("kenya_3_visits_url")
    kenya_3_patients_url = os.environ.get("kenya_3_patients_url")
    visits_1, patients_1 = get_kenya.read_access_data(kenya_1_url)
    visits_2, patients_2 = get_kenya.read_csv_data(kenya_2_visits_url,
                                                   kenya_2_patients_url)
    visits_3, patients_3 = get_kenya.read_csv_data(kenya_3_visits_url,
                                                   kenya_3_patients_url)

    data_ken_1 = get_kenya.format_tables(visits_1, patients_1, 'ken_fac_1')
    data_ken_2 = get_kenya.format_tables(visits_2, patients_2, 'ken_fac_2')
    data_ken_3 = get_kenya.format_tables(visits_3, patients_3, 'ken_fac_3')

haiti_metadata_url = os.environ.get("haiti_metadata_url")
haiti_metadata_url = 'data/raw/encBplus.txt'
# Loading Haiti
data_haiti = get_haiti.read_metadata(haiti_metadata_url)

# Combining all the data
if kenya == True :
    data_all = data_ken_1.append(data_ken_2).append(data_ken_3).append(data_haiti)

data_all = data_haiti
data_complete = data_all.dropna()

data_complete.to_csv('data/processed/complete_data.csv', index=False)

# TODO Check completeness of data exported from access to csv for Kenya 2 and 3
# IDEA Only load visit data ?
# TODO for Haiti, get dict of form types
# TODO format dates so they are all outputed in the same way
