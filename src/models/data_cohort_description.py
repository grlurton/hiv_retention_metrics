import pandas as pd

data = pd.read_csv('../../data/processed/complete_data.csv')
data = data.groupby('patient_id').apply(get_first_visit_date)


dat_2012 = data[data.first_visit_date < '2012-01-01']

ltfu_rates = []
for year in ['2012-01-01' , '2013-01-01' , '2014-01-01' , '2015-01-01' , '2016-01-01']:
    print(year)
    status_dat = dat_2012.groupby(['country' , 'facility' , 'patient_id']).apply(status_patient , reference_date = '2012-01-01' , analysis_date = year)
    perc_ltfu = status_dat.reset_index().groupby(['country' , 'facility' , 'analysis_date']).apply(get_ltfu_rate)
    if len(ltfu_rates) > 0 :
        ltfu_rates = ltfu_rates.append(perc_ltfu)
    if len(ltfu_rates) == 0 :
        ltfu_rates = status_dat.reset_index().groupby(['country' , 'facility' , 'analysis_date']).apply(get_ltfu_rate)

import matplotlib.pyplot as plt
%matplotlib inline

vl  = data.facility.value_counts()
for fac in vl.index :
    try :
        plt.plot(list(ltfu_rates[: , fac]) , 'k' , alpha = 0.09)
    except KeyError :
        continue
plt.show()
