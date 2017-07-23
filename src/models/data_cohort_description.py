import pandas as pd
import src.models.cohort_analysis_function as caf
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
import numpy as np

data = pd.read_csv('data/processed/complete_data.csv')
data = data[data.date_entered >= data.visit_date]
data = data.groupby('patient_id').apply(caf.get_first_visit_date)


dat_2012 = data[data.first_visit_date < '2012-01-01']

def perc_entered(data, date):
    data_to_enter = data[data.visit_date < date]
    return np.mean(data_to_enter.date_entered < date)

ltfu_rates = []
years = ['2012-01-01', '2013-01-01', '2014-01-01', '2015-01-01', '2016-01-01']
# TODO Parrallelize this
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

ltfu_rates.head()

# TODO move the outputting functions in a separate script, and just call here with conditional triggering

plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
for fac in list(vl.index):
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

ltfu_rates.head()

a = data1.groupby(['facility', 'visit_month']).delta_entry.median()
plt.figure(figsize=(30 , 30))
for i in range(120):
    plt.subplot(12, 10, (i + 1))
    try:
        dat = a[vl.index[i]]
        dat.plot()
    except (KeyError, ValueError , IndexError):
        continue

# Check : point of care arrive starting 2013-01

## How long does a patient stay in different status_dat

# Categories :
## 1. Followed
## 2. LTFU real
## 3. LTFU data
## 4. LTFU return
## 5. Other out

ids = data1.patient_id.unique()[12345]
pat1 = data1[(data1.patient_id == ids)]
pat1 = pat1.set_index(['patient_id' , 'date_entered']).sort_index()

data2 = data1.set_index(['patient_id' , 'date_entered']).sort_index()

def get_true_status(data_pat):
    date = []
    status_list = []
    data_pat = data_pat.reset_index().set_index(['patient_id' , 'date_entered']).sort_index()
    for data_entry_date in data_pat.index.levels[1] :
        if len(date) > 0 :
            delta = pd.to_datetime(data_entry_date) - pd.to_datetime(date_next)
            if delta.days <= 90:
                new_status = 'In Care'
            if delta.days > 90 :
                delta_visit = pd.to_datetime(data_pat.loc[(slice(None) , data_entry_date) , 'visit_date'].iloc[0]) -     pd.to_datetime(date_next)
                if delta_visit.days <= 90:
                    new_status = 'Data Entry LTFU'
                if delta_visit.days > 90 :
                    new_status = 'True LTFU'
            date_next = data_pat.loc[(slice(None) , data_entry_date)  , 'next_visit_date'].iloc[0]
            if new_status != status :
                status_list.append(new_status)
                date.append(data_entry_date)
                status = new_status
        if len(date) == 0 :
            date = [data_entry_date]
            status_list = ['In Care']
            status = 'In Care'
            date_next = min(data_pat.loc[(slice(None) , data_entry_date)  , 'next_visit_date'])
    out = pd.DataFrame({'date':date , 'status_list':status_list})
    out.date = pd.to_datetime(out.date)
    out['time'] = out.date.diff().shift(-1)
    out  = out.set_index('status_list')
    out.time = pd.to_numeric(out.time)
    return out

%%time
out = data2[2000000:2100000].groupby(level = 0).apply(get_true_status)

u = out.groupby(level = 1).time.apply(np.mean)
print(u)


# Until he finally exits care, a patient spends on average :

out.head()


def perc_time_status(data , total_time):
    return data.time.iloc[0] / total_time

def patient_distribution_status(data_patient):
    total_time = sum(data_patient.time.fillna(0))
    if len(data_patient) > 1 :
        time_distribution = data_patient.groupby(level = 1).apply(perc_time_status , total_time)
        return time_distribution

out.head()
t = out.groupby(level = 0).apply(patient_distribution_status)
t.head()
t.groupby(level = 1).fillna(0).apply(np.mean)

t.reset_index()
u[0] / sum(u)

out


# For each patient :
## 1. Start visit 1 => status 1
## 2. Look next visit :
##         a. if on time => check data entry
##              i. if on time => status 1
##              ii. if not on time => status 3
##         b. if not on time => status 4
## 3. Final outcome not important for now


## 2. Table :
    # col1 : date status change
    # col2 : new status




## Data Maturity : need metrics to evaluate performance
