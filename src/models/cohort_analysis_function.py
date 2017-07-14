import pandas as pd
import numpy as np

def get_first_visit_date(data_patient):
    data_patient['first_visit_date'] = min(data_patient.visit_date)
    return data_patient


def status_patient(data_patient, reference_date, analysis_date, grace_period):
    data_current = data_patient[data_patient.date_entered < analysis_date]
    reference_date = pd.to_datetime(reference_date)

    if len(data_current) > 0:
        date_last_appointment = max(data_current.next_visit_date)
        date_last_appointment = pd.to_datetime(date_last_appointment)
        late_time = reference_date - date_last_appointment
        if late_time.days > grace_period:
            status = 'LTFU'
        elif late_time.days <= grace_period:
            status = 'Followed'
        return pd.DataFrame([{'status': status,
                              'late_time': late_time,
                              'last_appointment': date_last_appointment,
                              'reference_date': reference_date,
                              'analysis_date': analysis_date}])


def get_ltfu_rate(patients_status_df):
    ltfu_perc = np.mean(patients_status_df.status == 'LTFU')
    return ltfu_perc


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
        return status


# QUESTION What is the validation of a LTFU patient ? Never comes back ? Comes
# back in less than a year ?
# QUESTION What are the form_types
# QUESTION Where are the other outcomes
# TODO refactor the functions :
# 1. Function to extract relevant data frame
# 2. Function to compute the needed quantity
# TODO Patient Object. fonction associee donne, pour une date donnee, un statut
# avec l'information disponible a ce moment la + le statut reel.
# TODO A given patient is on average wrongly considered LTFU XX% of the time if
# analysis conducted
# TODO Replication Chi ?
