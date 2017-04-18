def get_first_visit_date(data_patient):
    data_patient['first_visit_date'] = min(data_patient.visit_date)
    return data_patient

def status_patient(data  , reference_date , analysis_date  , grace_period = 90):
    data_current = data[data.date_entered < analysis_date]

    if len(data_current) > 0 :
        date_last_appointment = max(data_current.next_visit_date)

        late_time = pd.to_datetime(reference_date) - pd.to_datetime(date_last_appointment)
        if late_time.days > grace_period :
            status = 'LTFU'
        elif late_time.days <= grace_period :
            status = 'Followed'
        return pd.DataFrame([{'status':status , 'late_time':late_time , 'last_appointment':date_last_appointment , 'reference_date':reference_date , 'analysis_date':analysis_date}])

def get_ltfu_rate(patients_status_df):
    ltfu_perc = sum(patients_status_df.status == 'LTFU') / len(patients_status_df)
    return ltfu_perc

dat_2012 = data[data.first_visit_date < '2012-01-01']

len(dat_2012)

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

## QUESTION What is the validation of a LTFU patient ? Never comes back ? Comes back in less than a year ?
## TODO Patient Object. fonction associee donne, pour une date donnee, un statut avec l'information disponible a ce moment la + le statut reel.
## TODO A given patient is on average wrongly considered LTFU XX% of the time if analysis conducted
## TODO Replication Chi ?
