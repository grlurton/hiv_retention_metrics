import pandas as pd
import cohort_analysis_function as cohort_analysis


data = pd.read_csv('../../data/processed/complete_data.csv')
data = data.groupby('patient_id').apply(get_first_visit_date)

dat_2012 = data[data.first_visit_date < '2012-01-01']

ltfu_rates = []
for grace_period in [30 , 60 , 90 ,  180]:
    print(str(grace_period) + ' Days for definition')
    for year in ['2012-01-01' , '2013-01-01' , '2014-01-01' , '2015-01-01' , '2016-01-01']:
        print('Computing for ' + year)
        status_dat = dat_2012.groupby(['country' , 'facility' , 'patient_id']).apply(status_patient , reference_date = '2012-01-01' , analysis_date = year ,  grace_period = grace_period)
        status_dat['grace_period'] = grace_period
        perc_ltfu = status_dat.reset_index().groupby(['country' , 'facility' , 'analysis_date' , 'grace_period']).apply(get_ltfu_rate)
        if len(ltfu_rates) > 0 :
            ltfu_rates = ltfu_rates.append(perc_ltfu)
        if len(ltfu_rates) == 0 :
            ltfu_rates = status_dat.reset_index().groupby(['country' , 'facility' , 'analysis_date' , 'grace_period']).apply(get_ltfu_rate)

import matplotlib.pyplot as plt
%matplotlib inline

vl  = data.facility.value_counts()
plt.subplot(2, 2, 1)
for fac in vl.index :
    try :
        plt.plot(pd.to_datetime(list(ltfu_rates[:,fac,:,30].index.levels[1])) ,list(ltfu_rates[: , fac , : , 30]) , 'k' , alpha = 0.12)
    except (KeyError , ValueError):
        continue
plt.subplot(2, 2, 2)
for fac in vl.index :
    try :
        plt.plot(pd.to_datetime(list(ltfu_rates[:,fac,:,60].index.levels[1])) , list(ltfu_rates[: , fac , : , 60]) , 'b' , alpha = 0.12)
    except (KeyError , ValueError):
        continue
plt.subplot(2, 2, 3)
for fac in vl.index :
    try :
        plt.plot(pd.to_datetime(list(ltfu_rates[:,fac,:,90].index.levels[1])) ,list(ltfu_rates[: , fac , : , 90]) , 'r' , alpha = 0.12)
    except (KeyError , ValueError):
        continue
plt.subplot(2, 2, 4)
for fac in vl.index :
    try :
        plt.plot(pd.to_datetime(list(ltfu_rates[:,fac,:,180].index.levels[1])) , list(ltfu_rates[: , fac , : , 180]) , 'g' , alpha = 0.12)
    except (KeyError , ValueError):
        continue

plt.show()

plt.plot(ltfu_rates[:,fac,:,180].index.levels[1] ,list(ltfu_rates[: , fac , : , 30]) , 'k' , alpha = 0.12)

plt.plot(pd.to_datetime(list(ltfu_rates[:,fac,:,60].index.levels[1])) ,
list(ltfu_rates[: , fac , : , 60])z , 'b' , alpha = 0.12)

pd.to_datetime(list(ltfu_rates[:,fac,:,60].index.levels[1]))
list(ltfu_rates[: , fac , : , 60])
