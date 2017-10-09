import os
import src.data.get_kenya as get_kenya
import src.data.get_haiti as get_haiti

from dotenv import load_dotenv, find_dotenv

# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

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

haiti_data = os.environ.get("haiti_data")

haiti_metadata_url = haiti_data  + '/encBplus.txt'
haiti_disc_url = haiti_data + '/discBplus.txt'
# Loading Haiti
data_haiti = get_haiti.read_metadata(haiti_metadata_url, haiti_disc_url)


# Combining all the data
if kenya == True :
    data_all = data_ken_1.append(data_ken_2).append(data_ken_3).append(data_haiti)

data_all = data_haiti

data_all.to_csv('data/processed/complete_data.csv', index=False)

# TODO Check completeness of data exported from access to csv for Kenya 2 and 3
# TODO for Haiti, get dict of form types
# TODO format dates so they are all outputed in the same way
