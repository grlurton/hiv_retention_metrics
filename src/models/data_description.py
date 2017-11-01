import pandas as pd
import src.models.cohort_analysis_function as caf
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import subprocess
import os

%matplotlib inline

# TODO Replication Chi ?
# TODO Active patient summary by site. Isanté Team. Voir si on peut intégrer le résultat pour eux.
# TODO Faire un nombre de patient suivis, et un nombre de patients attendus


data = pd.read_csv('data/processed/complete_data.csv')
facilities_list = list(data.facility.unique())

caf.n_visits(data, '2013-01-01', '2013-02-01')

data = data.groupby('patient_id').apply(caf.get_first_visit_date)
data_report = data.groupby('patient_id').apply(caf.status_patient, '2013-01-01', '2015-02-01', 90)


import importlib
importlib.reload(caf);

data['first_visit_date'] = pd.to_datetime(data['first_visit_date'])
cohort = data[(data['first_visit_date'] >= pd.to_datetime('2007-01-01')) & (data['first_visit_date'] <= pd.to_datetime('2007-12-31'))]

caf.monthly_report(cohort, '2010-02-01', '2010-03-01', 90 , 365)

cohort['patient_id'] = cohort['patient_id'].apply(str)

data_follow_up = cohort.groupby('patient_id').apply(caf.horizon_outcome,  '2010-02-01', '2010-03-01', 90 , 365)
data_report = cohort.groupby('patient_id').apply(caf.status_patient, '2010-02-01', '2010-03-01', 90)

data_report.status.value_counts()


data_follow_up.status.value_counts()

data_follow_up.status_horizon.value_counts()

data_follow_up.status_horizon.value_counts()


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

## IDEA Data Maturity : need metrics to evaluate performance
