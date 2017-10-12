import pandas as pd
import ipyparallel

data = pd.read_csv('data/processed/complete_data.csv')
facilities_list = list(data.facility.unique())

def shift_date_next(data):
    data.sort_values(by = 'visit_date')
    data['actual_next_visit'] = data.visit_date.shift(-1)
    return data

### First,getting the daily probabilties of return for all patients

# ipcluster start -n 4
clients = ipyparallel.Client()
dview = clients[:]

shifted_data = data.groupby(['facility', 'patient_id']).apply(shift_date_next)
shifted_data['time_from_appointment'] = pd.to_datetime(shifted_data['actual_next_visit']) - pd.to_datetime(shifted_data['next_visit_date'])
shifted_data.time_from_appointment = shifted_data.time_from_appointment.dt.days

def run(delay, data = shifted_data):
    import pandas as pd
    def prop_delay(data, delay = delay):
        prop =  sum(data.time_from_appointment == delay) / (sum(data.time_from_appointment >= delay) + sum(pd.isnull(data.time_from_appointment)))
        return prop
    out = data.groupby('facility').apply(prop_delay)
    return out

return_probabilities = dview.map_sync(run, list(range(-90,365)))

return_tables = pd.DataFrame.from_dict(return_probabilities)
return_tables['delta'] = times
return_tables = return_tables.set_index('delta').stack()

return_tables.to_csv('data/processed/p_return_by_fac.csv')
