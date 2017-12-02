import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta

#### Utilities

def get_first_visit_date(data_patient):
    ''' Determines the first visit for a given patient'''
    #IDEA Could be parallelized in Dask
    data_patient['first_visit_date'] = min(data_patient.visit_date)
    return data_patient

def subset_analysis_data(data, date_analysis):
    ''' Function that subsets the full dataset to only the data available for a certain analysis date'''
    if type(data.date_entered.iloc[0]) is str :
        data.date_entered = pd.to_datetime(data.date_entered)
    data = data[data.date_entered < date_analysis]
    return data

def subset_cohort(data, horizon_date, horizon_time, bandwidth):
    ''' Function that subsets data from a cohort that has initiated care a year before the horizon_date, and after a year + bandwith'''
    horizon_date = pd.to_datetime(horizon_date)
    data['first_visit_date'] = pd.to_datetime(data['first_visit_date'])
    cohort_data = data[(data['first_visit_date'] >= horizon_date - relativedelta(days=horizon_time + bandwidth)) &
                 (data['first_visit_date'] < horizon_date - relativedelta(days=horizon_time))]
    return cohort_data


#### Standard reporting

def status_patient(data_patient, reference_date, grace_period):
    ''' Determines the status of a patient at a given reference_date, given the data available at a given analysis_date
    TODO Also select the available data for Death and Transfer and other outcomes based on data entry time
    '''
    #IDEA Could be parallelized in Dask
    data_patient = get_first_visit_date(data_patient)
    date_out = pd.NaT
    date_last_appointment = pd.to_datetime(max(data_patient.next_visit_date))
    late_time = reference_date - date_last_appointment
    if late_time.days > grace_period:
        status = 'LTFU'
        date_out = date_last_appointment
    if late_time.days <= grace_period:
        status = 'Followed'
    if (data_patient.reasonDescEn.iloc[0] is not np.nan) & (pd.to_datetime(data_patient.discDate.iloc[0]) < reference_date):
        status = data_patient.reasonDescEn.iloc[0]
        date_out = pd.to_datetime(data_patient.discDate.iloc[0])
    return pd.DataFrame([{'status': status,
                          'late_time': late_time,
                          'last_appointment': date_last_appointment,
                          'date_out':date_out ,
                          'first_visit_date':data_patient.first_visit_date.iloc[0],
                          'facility':data_patient.facility.iloc[0]}])

def horizon_outcome(data_cohort, reference_date, horizon_time):
    # TODO Make sure dates are dates
    data_cohort['first_visit_date'] = pd.to_datetime(data_cohort['first_visit_date']) #TODO This conversion should happen earlier

    data_cohort.loc[:, 'horizon_date'] = data_cohort['first_visit_date'] + np.timedelta64(horizon_time, 'D')
    data_cohort.loc[: , 'horizon_status'] = data_cohort['status']
    # If the patient exited the cohort after his horizon date, still consider him followed
    # BUG This is marginally invalid, for example if a patient was considered LTFU before he died
    data_cohort.horizon_status[~(data_cohort['status'] == 'Followed') & (data_cohort['date_out'] > data_cohort['horizon_date'])] = 'Followed'
    return data_cohort


## Transversal description only
def n_visits(data, month):
    reporting_month = pd.to_datetime(data['visit_date']).dt.to_period('M')
    n_vis =  sum(reporting_month == month)
    return n_vis

def make_report(data, reference_date, date_analysis, grace_period, horizon_time, cohort_width):
    assert reference_date <= date_analysis, 'You should not analyze a period before you have the data (date of analysis is before reference date)'
    if type(reference_date) is str :
        reference_date = pd.to_datetime(reference_date)
    if type(date_analysis) is str:
        date_analysis = pd.to_datetime(date_analysis)
    report_data = subset_analysis_data(data, date_analysis)
    if len(report_data) > 0:
        month = reference_date.to_period('M') - 1
        n_visits_month = report_data.groupby('facility').apply(n_visits, month)
        df_status = report_data.groupby('patient_id').apply(status_patient, reference_date, 90)
        cohort_data = subset_cohort(df_status, reference_date, horizon_time, cohort_width)
    #    print(df_status.head())
        horizon_outcome_data = horizon_outcome(cohort_data, month, 365)
        transversal_reports = df_status.groupby('facility').status.value_counts()
        longitudinal_reports = horizon_outcome_data.groupby('facility').status.value_counts()
        out_reports = {'transversal':transversal_reports,
                        'longitudinal':longitudinal_reports,
                        'n_visits':n_visits_month}
        return out_reports

# QUESTION What are the form_types
