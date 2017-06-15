import pandas as pd
import src.models.cohort_analysis_function as caf
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline


data = pd.read_csv('data/processed/complete_data.csv')
data = data[data.date_entered >= data.visit_date]
data = data.groupby('patient_id').apply(caf.get_first_visit_date)


dat_2012 = data[data.first_visit_date < '2012-01-01']


def perc_entered(data, date):
    data_to_enter = data[data.visit_date < date]
    return np.mean(data_to_enter.date_entered < date)


data.groupby('facility').apply(perc_entered, date='2012-01')

ltfu_rates = []
years = ['2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01']
for grace_period in [30, 60, 90,  180]:
    print(str(grace_period) + ' Days for definition')
    for year in years:
        print('Computing for ' + year)
        status_dat = dat_2012.groupby(['country', 'facility', 'patient_id'])
        status_dat = status_dat.apply(caf.status_patient,
                                      reference_date='2012-01-01',
                                      analysis_date=year,
                                      grace_period=grace_period)
        status_dat['grace_period'] = grace_period
        perc_ltfu = status_dat.reset_index()
        perc_ltfu = perc_ltfu.groupby(['country', 'facility',
                                       'analysis_date', 'grace_period'])
        perc_ltfu = perc_ltfu.apply(caf.get_ltfu_rate)
        if len(ltfu_rates) > 0:
            ltfu_rates = ltfu_rates.append(perc_ltfu)
        if len(ltfu_rates) == 0:
            ltfu_rates = status_dat.reset_index()
            ltfu_rates = ltfu_rates.groupby(['country', 'facility',
                                            'analysis_date', 'grace_period'])
            ltfu_rates = ltfu_rates.apply(caf.get_ltfu_rate)

vl = data.facility.value_counts()

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
plt.savefig('reports/figures/impact_definition.png')

a = pd.to_datetime(data.date_entered)

data['delta_entry'] = pd.to_datetime(data.date_entered) - pd.to_datetime(data.visit_date)
data['delta_entry'] = data.delta_entry.dt.days
data['visit_month'] = pd.to_datetime(data.visit_date).dt.to_period(freq='A')
data1 = data[(data['delta_entry'] >= 0) & (data['delta_entry'] <630)]


plt.hist(data1.delta_entry, bins=52);

a = data1.groupby(['facility', 'visit_month']).delta_entry.median()
for fac in vl.index[0:250]:
    try:
        a[fac].plot()
    except (KeyError, ValueError):
        continue


plt.figure(figsize=(30 , 30))
for i in range(120):
    plt.subplot(12, 10, (i + 1))
    try:
        dat = a[vl.index[i]]
        dat.plot()
    except (KeyError, ValueError):
        continue
