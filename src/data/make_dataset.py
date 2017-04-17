import os
from dotenv import load_dotenv, find_dotenv
import get_kenya
import get_haiti


# find .env automagically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

kenya_1_url = os.environ.get("kenya_1_url")
kenya_2_visits_url = os.environ.get("kenya_2_visits_url")
kenya_2_patients_url = os.environ.get("kenya_2_patients_url")
kenya_3_visits_url = os.environ.get("kenya_3_visits_url")
kenya_3_patients_url = os.environ.get("kenya_3_patients_url")

haiti_metadata_url = os.environ.get("haiti_metadata_url")

### Loading Kenya
visits_1 , patients_1 = get_kenya.read_access_data(kenya_1_url)
visits_2 , patients_2 = get_kenya.read_csv_data(kenya_2_visits_url , kenya_2_patients_url)
visits_3 , patients_3 = get_kenya.read_csv_data(kenya_3_visits_url , kenya_3_patients_url)

data_ken_1 = get_kenya.format_tables(visits_1 , patients_1 , 'ken_fac_1')
data_ken_2 = get_kenya.format_tables(visits_2 , patients_2 , 'ken_fac_2')
data_ken_3 = get_kenya.format_tables(visits_3 , patients_3 , 'ken_fac_3')

### Loading Haiti
data_haiti = get_haiti.read_metadata(haiti_metadata_url)


## Combining all the data
data_all = data_ken_1.append(data_ken_2).append(data_ken_3).append(data_haiti)
data_complete = data_all.dropna()

### TODO Check completeness of data exported from access to csv for Kenya facilities 2 and 3
### IDEA Only load visit data ?
### TODO for Haiti, get dict of form types
