import pandas as pd


data = pd.read_csv('../../data/processed/complete_data.csv')

data['data_entry_time'] = pd.to_datetime(data.visit_date) - pd.to_datetime(data.date_entered)
data['visit_time'] = pd.to_datetime(data.next_visit_date) - pd.to_datetime(data.visit_date)


def status_patient(data  , analysis_date = '2012-01-01' , grace_period = 90):
    if analysis_date is None :
        analysis_date = max(data.date_entered)

    final_visit = max(data.next_visit_date)
    data_current = data[data.date_entered < analysis_date]

    if len(data_current) > 0 :
        date_last_appointment = max(data_current.next_visit_date)

        late_time = pd.to_datetime(analysis_date) - pd.to_datetime(date_last_appointment)
        if late_time.days > grace_period :
            status = 'LTFU'
        elif late_time.days <= grace_period :
            status = 'Followed'

        if final_visit == date_last_appointment :
            true_status = status
        elif final_visit != date_last_appointment :
            true_status = 'Followed'


        return pd.DataFrame([{'status':status , 'late_time':late_time , 'last_appointment':date_last_appointment , 'true_status':true_status}])

%%time
u = data.groupby(['country' ,'patient_id']).apply(status_patient , analysis_date = '2011-01-01')

u.status.groupby(level =0).value_counts()

sum(u.status != u.true_status)/len(u)

## QUESTION What is the validation of a LTFU patient ? Never comes back ? Comes back in less than a year ?
## TODO Patient Object. fonction associee donne, pour une date donnee, un statut avec l'information disponible a ce moment la + le statut reel.
## TODO A given patient is on average wrongly considered LTFU XX% of the time if analysis conducted
## TODO Replication Chi ?
