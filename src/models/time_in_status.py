

# TODO A given patient is on average wrongly considered LTFU XX% of the time if

## How long does a patient stay in different status_dat

# Categories :
## 1. Followed
## 2. LTFU real
## 3. LTFU data
## 4. LTFU return
## 5. Other out

## Change to make : for patient who are Data Entry LTFU have the change of status happen right after the data is entered. Ie : 2 dates have to be added / 2 periods
def get_true_status(data_pat):
    date = []
    status_list = []
    data_pat = data_pat.reset_index().set_index(['patient_id' , 'date_entered']).sort_index()
    final_visit = max(data_pat.visit_date)
    for data_entry_date in data_pat.index.levels[1] :
        visit_date = data_pat.loc[(slice(None) , data_entry_date) , 'visit_date'].iloc[0]
        ltfu_date = pd.to_datetime(visit_date) + timedelta(days=90)
        if len(date) > 0 :
            delta = pd.to_datetime(data_entry_date) - pd.to_datetime(date_next)
            if delta.days <= 90:
                new_status = 'In Care'
            if delta.days > 90 :
                delta_visit = pd.to_datetime(visit_date) - pd.to_datetime(date_next)
                if delta_visit.days <= 90:
                    new_status = 'Data Entry LTFU'
                if delta_visit.days > 90 :
                    new_status = 'Temporary LTFU'
            if new_status != status :
                status_list.append(new_status)
                date.append(data_entry_date)
                status = new_status
        if len(date) == 0 :
            date = [data_entry_date]
            status_list = ['In Care']
            status = 'In Care'
            date_next = min(data_pat.loc[(slice(None) , data_entry_date)  , 'next_visit_date'])
    out = pd.DataFrame({'date':date , 'status_list':status_list})
    out.date = pd.to_datetime(out.date)
    out['time'] = out.date.diff().shift(-1)
    out  = out.set_index('status_list')
    out.time = pd.to_numeric(out.time)
    return out

out = data2[2000000:2010000].groupby(level = 0).apply(get_true_status)
u = out.groupby(level = 1).time.apply(np.mean)

# Until he finally exits care, a patient spends on average :
def perc_time_status(data , total_time):
    return data.time.iloc[0] / total_time

def patient_distribution_status(data_patient):
    total_time = sum(data_patient.time.fillna(0))
    if len(data_patient) > 1 :
        time_distribution = data_patient.groupby(level = 1).apply(perc_time_status , total_time)
        return time_distribution

t = out.groupby(level = 0).apply(patient_distribution_status)
t.columns = ['perc']

t.groupby(level = 1).mean()


# For each patient :
## 1. Start visit 1 => status 1
## 2. Look next visit :
##         a. if on time => check data entry
##              i. if on time => status 1
##              ii. if not on time => status 3
##         b. if not on time => status 4
## 3. Final outcome not important for now


## 2. Table :
    # col1 : date status change
    # col2 : new status
