import pandas as pd
import src.models.cohort_analysis_function as caf
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import ipyparallel
import subprocess
import os

%matplotlib inline

data = pd.read_csv('data/processed/complete_data.csv')
facilities_list = list(data.facility.unique())


caf.n_visits(data, '2013-01-01', '2013-02-01')
data = data.groupby('patient_id').apply(caf.get_first_visit_date)
data_report = data.groupby('patient_id').apply(caf.status_patient, '2013-01-01', '2015-02-01', 90)

data_report.status.value_counts()


# TODO N Suivi vs N came last month
# TODO N Suivi vs N coming next month
# TODO move the outputting functions in a separate script, and just call here with conditional triggering

## Looking at data entry times

data['delta_entry'] = pd.to_datetime(data.date_entered) - pd.to_datetime(data.visit_date)
data['delta_entry'] = data.delta_entry.dt.days
data['visit_year'] = pd.to_datetime(data.visit_date).dt.to_period(freq='A')
censored_data_entry = data[(data['delta_entry'] >= 0) & (data['delta_entry'] <630)]

data_entry_evolution = censored_data_entry.groupby(['facility', 'visit_year']).delta_entry.median()

plt.figure(figsize=(20 , 20))
for i in range(len(facilities_list)):
    plt.subplot(12, 10, (i + 1))
    try:
        fac_data = data_entry_evolution[facilities_list[i]]
        fac_data.plot()
    except (KeyError, ValueError , IndexError):
        continue

plt.figure(figsize=(20 , 20))
for i in range(len(facilities_list)):
    plt.subplot(12, 10, (i + 1))
    try:
        fac_data = censored_data_entry[censored_data_entry.facility == facilities_list[i]]
        plt.hist(fac_data.delta_entry, bins=52);
    except (KeyError, ValueError , IndexError):
        continue

# QUESTION point of care data entry arrive starting 2013-01 : can we see it in the data entry data ?

# Probability of patient coming back on a given date knowing he didn't come earlier
def shift_date_next(data):
    data.sort_values(by = 'visit_date')
    data['actual_next_visit'] = data.visit_date.shift(-1)
    return data

# ipcluster start -n 4
clients = ipyparallel.Client()
dview = clients[:]

shifted_data = data.groupby(['facility', 'patient_id']).apply(shift_date_next)
shifted_data['time_from_appointment'] = pd.to_datetime(shifted_data['actual_next_visit']) - pd.to_datetime(shifted_data['next_visit_date'])
shifted_data.time_from_appointment = shifted_data.time_from_appointment.dt.days

def run(delay, data = shifted_data):
    import pandas as pd
    def prop_delay(data, delay = delay):
        prop =  sum(data.time_from_appointment == delay) / (sum(data.time_from_appointment >= delay) + sum(pd.isnull(data.time_from_appointment)))
        return prop
    out = data.groupby('facility').apply(prop_delay)
    return out

return_probabilities = dview.map_sync(run, list(range(-90,365)))

return_tables = pd.DataFrame.from_dict(return_probabilities)
return_tables['delta'] = times
return_tables = return_tables.set_index('delta').stack()

return_tables.to_csv('data/processed/p_return_by_fac.csv')

## IDEA Data Maturity : need metrics to evaluate performance
