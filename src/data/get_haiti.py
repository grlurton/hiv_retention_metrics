import pandas as pd

metadata_columns_to_keep = ['patientid' , 'sitecode' , 'form_id' , 'visitdate' , 'nxtVisitDate' , 'createdate']

def read_metadata(haiti_metadata_url, haiti_disc_url, metadata_columns_to_keep=metadata_columns_to_keep):
    metadata = pd.read_csv(haiti_metadata_url , sep = '|')
    metadata = metadata[metadata_columns_to_keep]
    metadata.createdate = pd.to_datetime(metadata.createdate , errors = 'coerce')
    metadata.visitdate = pd.to_datetime(metadata.visitdate , errors = 'coerce')
    metadata.nxtVisitDate = pd.to_datetime(metadata.nxtVisitDate , errors = 'coerce')

    # Adding in the discontinuation data
    disc_data = pd.read_csv(haiti_disc_url, sep = '|')
    data = metadata.merge(disc_data)

    data.columns = ['patient_id' , 'facility' , 'form_type' , 'visit_date' , 'next_visit_date' , 'date_entered', 'discDate', 'discType', 'reasonDescEn']
    data['country'] = 'Haiti'
    return data
