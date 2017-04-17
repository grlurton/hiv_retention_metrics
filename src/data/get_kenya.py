import pyodbc
import pandas as pd
import datetime

visits_columns_to_keep = ['patient_id' , 'visit_date' , 'next_visit_date' , 'DateEntered']
patients_columns_to_keep = ['patient_id' , 'date_entered']

def read_access_data(access_db_url , visits_columns_to_keep=visits_columns_to_keep , patients_columns_to_keep=patients_columns_to_keep):
    sql_visits = 'select ' + ' , '.join(visits_columns_to_keep) + ' from tblvisit_information'
    sql_patients = 'select ' + ' , '.join(patients_columns_to_keep) + ' from tblpatient_information'

    conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)}; '
    r'DBQ='+ access_db_url +';'
    )
    connexion = pyodbc.connect(conn_str)

    visits = pd.read_sql(sql_visits , connexion)
    patients = pd.read_sql(sql_patients , connexion)

    visits_columns_to_keep = [item.lower() for item in visits_columns_to_keep]
    patients_columns_to_keep = [item.lower() for item in patients_columns_to_keep]

    visits.columns = visits_columns_to_keep
    patients.columns = patients_columns_to_keep

    return (visits , patients)

def read_csv_data(csv_visits_url , csv_patients_url, visits_columns_to_keep=visits_columns_to_keep , patients_columns_to_keep=patients_columns_to_keep):
    visits_columns_to_keep = [item.lower() for item in visits_columns_to_keep]
    patients_columns_to_keep = [item.lower() for item in patients_columns_to_keep]
    visits = pd.read_csv(csv_visits_url , encoding = "ISO-8859-1")
    patients = pd.read_csv(csv_patients_url  , encoding = "ISO-8859-1")
    visits = visits[visits_columns_to_keep]
    patients = patients[patients_columns_to_keep]
    return (visits , patients)

def format_tables(table_visits , table_patients , fac_id):
    table_visits.dateentered = pd.to_datetime(table_visits.dateentered)
    table_visits.visit_date = pd.to_datetime(table_visits.visit_date , errors='coerce')
    table_visits.next_visit_date = pd.to_datetime(table_visits.next_visit_date , errors='coerce')
    table_visits.patient_id = fac_id + '_' + table_visits.patient_id.astype('str')
    table_visits['facility'] = fac_id
    table_visits['form_type'] = 'visit'
    table_visits.columns = ['patient_id', 'visit_date', 'next_visit_date', 'date_entered', 'facility', 'form_type']

    table_patients.date_entered = pd.to_datetime(table_patients.date_entered)
    table_patients['facility'] = fac_id
    table_patients['form_type'] = 'patient'

    out_table = table_patients.append(table_visits)
    out_table['country'] = 'Kenya'
    return out_table
