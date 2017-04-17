
#################################################################################################################
def make_patient_data(data):
    first_visit = min(data.visit_date)
    time_follow_up = data.visit_date - first_visit
    time_follow_up = time_follow_up.tolist()
    data = data.sort_values('visit_date' , ascending = True)
    last_given_appointment = [pd.NaT] + data.next_visit_date[1:len(data)].tolist()
    return pd.DataFrame({'first_visit':first_visit , 'time_follow_up':time_follow_up ,
                            'last_given_appointment':last_given_appointment})

visits_all = visits_all.set_index(['patient_id'])

visits = visits_all.groupby(level = 0).apply(make_patient_data)

a = list(np.random.choice(list(visits.index.levels[0]) , 50))

u = visits.loc[a].reset_index()
#################################################################################################################
import numpy as np
import seaborn as sns
sns.set(style="white", palette="muted", color_codes=True)
%matplotlib inline


u.time_follow_up = u.time_follow_up.dt.days
u = u[u.time_follow_up < 365]

sns.stripplot(y = 'patient_id' , x = 'time_follow_up' , data = u)

for id_num in range(vis.patient_id.nunique()) :
    id_patient = vis.patient_id.unique()[id_num]
    plt.plot(vis.patient_id , vis.time_schedule)




visits['visit_entry'] = visits.dateentered - visits.visit_date
visits['visit_entry'] = visits['visit_entry'].astype('timedelta64[D]').astype(int , raise_on_error=False)
visit_entry_toplot = visits['visit_entry']
visit_entry_toplot = visit_entry_toplot[~(pd.isnull(visit_entry_toplot)) & (visit_entry_toplot < 100) & (visit_entry_toplot >= 0)]

import matplotlib
import matplotlib.pyplot as plt
def set_style():
    plt.style.use(['seaborn-white', 'seaborn-paper'])
    matplotlib.rc("font", family="Times New Roman")
    sns.set_palette(get_colors())

def get_colors():
    return np.array([
        [0.639,0.176,0.114],            # Red
        [0.078,0.337,0.396],            # Blue
        [0.086,0.478,0.188],            # Green
        [0.639,0.376,0.114],            # Brun
        [0.984375, 0.7265625, 0],       # Yellow
    ])

def set_size(fig):
    fig.set_size_inches(6, 3)
    plt.tight_layout()

visit_entry_toplot = visit_entry_toplot.reset_index()

set_style()
sns.set_context("paper")
plt.figure(figsize=(6, 3))
g = sns.FacetGrid(visit_entry_toplot, col="facility",  size=2 , sharey = False , sharex = False)
g = g.map(plt.hist, "visit_entry" , bins = 20 , normed = True)
g.set(xlabel='Days between visit and data entry')
sns.plt.xlim(0,)
#ax.figure.savefig("figure/data_entry_time.pdf", dpi=1200)

visits['time_schedule']  = visits.next_visit_date - visits.visit_date
visits['time_schedule'] = visits['time_schedule'].astype('timedelta64[D]').astype(int , raise_on_error=False)
visit_schedule_toplot = visits['time_schedule']
visit_schedule_toplot  = visit_schedule_toplot[(~pd.isnull(visit_schedule_toplot)) & (visit_schedule_toplot < 150) & (visit_schedule_toplot > 0)]

plt.figure(figsize=(6, 3))
ax = sns.distplot(visit_schedule_toplot , kde = False )
ax.set(xlabel='Days between visit and next scheduled appointment')
sns.plt.xlim(0,)
#ax.figure.savefig("figure/time_to_appointment.pdf", dpi=1200)

late_to_appointment = (visits_1.last_given_appointment-visits_1.visit_date).astype('timedelta64[D]').astype(int , raise_on_error=False)
late_to_appointment = late_to_appointment[(~pd.isnull(late_to_appointment)) & (np.abs(late_to_appointment) < 250)] % 28

plt.figure(figsize=(6, 3))
ax = sns.distplot(late_to_appointment , kde = False)
ax.set(xlabel='Days late to appointment')
sns.plt.xlim(0,)
#ax.figure.savefig("figure/time_late_to_appointment.pdf", dpi=1200)
