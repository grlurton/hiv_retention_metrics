import pandas as pd

metadata_columns_to_keep = ['patientid' , 'sitecode' , 'form_id' , 'visitdate' , 'nxtVisitDate' , 'createdate']

def read_metadata(haiti_metadata_url , metadata_columns_to_keep=metadata_columns_to_keep):
    metadata = pd.read_csv(haiti_metadata_url , sep = '|')
    metadata = metadata[metadata_columns_to_keep]
    metadata.createdate = pd.to_datetime(metadata.createdate , errors = 'coerce')
    metadata.visitdate = pd.to_datetime(metadata.visitdate , errors = 'coerce')
    metadata.nxtVisitDate = pd.to_datetime(metadata.nxtVisitDate , errors = 'coerce')
    metadata.columns = ['patient_id' , 'facility' , 'form_type' , 'visit_date' , 'next_visit_date' , 'date_entered']
    metadata['country'] = 'Haiti'
    return metadata
