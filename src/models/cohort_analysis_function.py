import pandas as pd
import numpy as np

#### Utilities

def get_first_visit_date(data_patient):
    data_patient['first_visit_date'] = min(data_patient.visit_date)
    return data_patient

#### Standard reporting

def status_patient(data_patient, reference_date, analysis_date, grace_period):
    ''' Determines the status of a patient at a given reference_date, given the data available at a given analysis_date
    TODO Also select the available data for Death and Transfer and other outcomes based on data entry time
    '''
    data_current = data_patient[data_patient.date_entered < analysis_date]
    reference_date = pd.to_datetime(reference_date)

    if len(data_current) > 0:
        date_out = pd.NaT
        date_last_appointment = max(data_current.next_visit_date)
        date_last_appointment = pd.to_datetime(date_last_appointment)
        late_time = reference_date - date_last_appointment
        if late_time.days > grace_period:
            status = 'LTFU'
            date_out = date_last_appointment
        if late_time.days <= grace_period:
            status = 'Followed'
        if (data_current.reasonDescEn.iloc[0] is not np.nan) & \
        (pd.to_datetime(data_current.discDate.iloc[0]) < reference_date):
            status = data_current.reasonDescEn.iloc[0]
            date_out = pd.to_datetime(data_current.discDate.iloc[0])
        return pd.DataFrame([{'status': status,
                              'late_time': late_time,
                              'last_appointment': date_last_appointment,
                              'reference_date': reference_date,
                              'analysis_date': analysis_date,
                              'date_out':date_out,
                              'first_visit_date':data_current.first_visit_date.iloc[0]}])

def horizon_outcome(data_patient, reference_date, analysis_date,
                    grace_period, horizon):
    reference_date = pd.to_datetime(reference_date)
    data_patient['first_visit_date'] = pd.to_datetime(
                data_patient['first_visit_date'])
    length_suivi = reference_date - data_patient.iloc[0]['first_visit_date']
    length_suivi = length_suivi.days
    if length_suivi < horizon:
        pass
    if length_suivi >= horizon:
        status = status_patient(data_patient, reference_date,
                                analysis_date, grace_period)
        if status is not None:
            if status.date_out.iloc[0] is not pd.NaT:
                time = status.date_out - status.first_visit_date
                if time.iloc[0].days <= horizon:
                    status['status_horizon'] = status.status
                if time.iloc[0].days > horizon:
                    status['status_horizon'] = 'Followed'
            if status.date_out.iloc[0] is pd.NaT:
                status['status_horizon'] = 'Followed'
            return status

## Transversal description only
def n_visits(data, month, analysis_date):
    month = pd.to_datetime(month).to_period('M')
    data['reporting_month'] = pd.to_datetime(data['visit_date']).dt.to_period('M')
    analyse_data = data[(data['reporting_month'] == month) &
                        (data['date_entered'] < analysis_date)]
    return len(analyse_data)





# QUESTION What are the form_types
# TODO regorganize the code in different types of reports and utilities functions
# TODO refactor the functions :
# 1. Function to extract relevant data frame based on date of analysis
# 2. Function to compute the needed quantities
# TODO A given patient is on average wrongly considered LTFU XX% of the time if
# analysis conducted
# TODO Replication Chi ?

# Active patient summary by site. Isanté Team. Voir si on peut intégrer le résultat pour eux.
# TODO Faire un nombre de patient suivis, et un nombre de patients attendus
