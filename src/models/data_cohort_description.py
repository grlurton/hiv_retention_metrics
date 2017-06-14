import pandas as pd
from cohort_analysis_function import *
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline


data = pd.read_csv('../../data/processed/complete_data.csv')
data = data.groupby('patient_id').apply(get_first_visit_date)

dat_2012 = data[data.first_visit_date < '2012-01-01']

ltfu_rates = []
years = ['2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01']
for grace_period in [30, 60, 90,  180]:
    print(str(grace_period) + ' Days for definition')
    for year in years:
        print('Computing for ' + year)
        status_dat = dat_2012.groupby(['country', 'facility', 'patient_id'])
        status_dat = status_dat.apply(status_patient,
                                      reference_date='2012-01-01',
                                      analysis_date=year,
                                      grace_period=grace_period)
        status_dat['grace_period'] = grace_period
        perc_ltfu = status_dat.reset_index()
        perc_ltfu = perc_ltfu.groupby(['country', 'facility',
                                       'analysis_date', 'grace_period'])
        perc_ltfu = perc_ltfu.apply(get_ltfu_rate)
        if len(ltfu_rates) > 0:
            ltfu_rates = ltfu_rates.append(perc_ltfu)
        if len(ltfu_rates) == 0:
            ltfu_rates = status_dat.reset_index()
            ltfu_rates = ltfu_rates.groupby(['country', 'facility',
                                            'analysis_date', 'grace_period'])
            ltfu_rates = ltfu_rates.apply(get_ltfu_rate)


vl = data.facility.value_counts()

font = {'family': 'times',
        'weight': 'normal',
        'size': 8}

matplotlib.rc('font', **font)
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
for fac in vl.index:
    try:
        plt.plot(
            pd.to_datetime(list(ltfu_rates[:, fac, :, 30].index.levels[1])),
            list(ltfu_rates[:, fac, :, 30]), 'k', alpha=0.12)
        plt.title('30 Days Definition')
    except (KeyError, ValueError):
        continue
plt.subplot(2, 2, 2)
for fac in vl.index:
    try:
        plt.plot(
            pd.to_datetime(list(ltfu_rates[:, fac, :, 60].index.levels[1])),
            list(ltfu_rates[:, fac, :, 60]), 'b', alpha=0.12
            )
        plt.title('60 Days Definition')
    except (KeyError, ValueError):
        continue
plt.subplot(2, 2, 3)
for fac in vl.index:
    try:
        plt.plot(
            pd.to_datetime(list(ltfu_rates[:, fac, :, 90].index.levels[1])),
            list(ltfu_rates[:, fac, :, 90]), 'r', alpha=0.12
            )
        plt.title('90 Days Definition')
    except (KeyError, ValueError):
        continue
plt.subplot(2, 2, 4)
for fac in vl.index:
    try:
        plt.plot(
            pd.to_datetime(list(ltfu_rates[:, fac, :, 180].index.levels[1])),
            list(ltfu_rates[:, fac, :, 180]), 'g', alpha=0.12
            )
        plt.title('120 Days Definition')
    except (KeyError, ValueError):
        continue
plt.savefig('../../reports/figures/impact_definition.png')

plt.plot(ltfu_rates[:, fac, :, 180].index.levels[1],
         list(ltfu_rates[:, fac, :, 30]), 'k', alpha=0.12)

plt.plot(pd.to_datetime(list(ltfu_rates[:, fac, :, 60].index.levels[1])),
         list(ltfu_rates[:, fac, :, 60]), 'b', alpha=0.12)

pd.to_datetime(list(ltfu_rates[:, fac, :, 60].index.levels[1]))
list(ltfu_rates[:, fac, :, 60])
