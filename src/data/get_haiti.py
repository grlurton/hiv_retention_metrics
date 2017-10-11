import pandas as pd
import numpy as np

metadata_columns_to_keep = ['patientid' , 'sitecode' , 'form_id' , 'visitdate' , 'nxtVisitDate' , 'createdate']

def read_haiti_data(haiti_metadata_url, haiti_disc_url, metadata_columns_to_keep=metadata_columns_to_keep):
    metadata = pd.read_csv(haiti_metadata_url , sep = '|')
    metadata = metadata[metadata_columns_to_keep]
    metadata.createdate = pd.to_datetime(metadata.createdate , errors = 'coerce')
    metadata.visitdate = pd.to_datetime(metadata.visitdate , errors = 'coerce')
    metadata.nxtVisitDate = pd.to_datetime(metadata.nxtVisitDate , errors = 'coerce')
    print('Metadata ' + str(len(metadata)))
    metadata = metadata.dropna()
    print('Metadata no NA ' + str(len(metadata)))

    # Adding in the discontinuation data
    disc_data = pd.read_csv(haiti_disc_url, sep = '|')
    disc_data.discDate = pd.to_datetime(disc_data.discDate , errors = 'coerce')

    data = metadata.merge(disc_data , how = 'left')

    data.columns = ['patient_id' , 'facility' , 'form_type' , 'visit_date' , 'next_visit_date' , 'date_entered', 'discDate', 'discType', 'reasonDescEn']
    data['country'] = 'Haiti'

    data.loc[data.reasonDescEn.isin(['Patient preference', 'Seroreversion',
                                    'Poor adherence', 'Stock out']) , 'reasonDescEn'] = 'Other reasons'
    data.loc[data.reasonDescEn == 'Patient moved', 'reasonDescEn'] = 'Transferred'
    data.loc[data.reasonDescEn.isin(['Loss of contact more than 3 months', 'Unknown reason'])] = np.NaN


    print('Final ' + str(len(data)))

    return data
