import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import src.models.cohort_analysis_function as caf
from dateutil.relativedelta import relativedelta
import ipyparallel as ipp
import itertools

%matplotlib inline

data = pd.read_csv('data/processed/complete_data.csv')

def make_dates_sequence(start, end, frequence_analysis='YS'):
    date_reference_list = list(pd.date_range(start=start, end=end, freq='MS'))
    date_analysis_list = list(pd.date_range(start=start, end=end, freq=frequence_analysis))
    combination_list = []
    for date_a in date_reference_list :
        for date_b in date_analysis_list :
            if date_a <= date_b:
                combination_list = combination_list + [[date_a, date_b]]
    return combination_list

def run_trail(point, data=data):
    reference_date = point[0]
    analysis_date = point[1]
    out = make_report(data, reference_date, analysis_date, 90, 365, 365)
    return {reference_date:{analysis_date:out}}

analysis_points = make_dates_sequence('2007-01-01', '2017-01-01', frequence_analysis='YS')

rc = ipp.Client()
all_engines = rc[:]
view = rc.load_balanced_view()
import os
%px import os; os.chdir("{os.getcwd()}")

all_engines.push(dict(
    make_report=caf.make_report
))

all_engines.block = True

data_processed = all_engines.map_async(run_trail, analysis_points)

%%time
data_processed.wait_interactive(interval = 60)


data_to_tab = data_processed.get()

def extract_section(report, section_name):
    section = pd.DataFrame({'date':date_report, 'analysis':date_analysis, section_name:reports[section_name]})
    section = section.set_index(['date','analysis'], drop=True, append=True, inplace=False)
    section = section.stack()
    section = pd.DataFrame(data=section)
    if len(section.index.levels) == 5:
        section.index.rename(['facility', 'status', 'date', 'analysis', 'type'] , inplace=True)
    if len(section.index.levels) == 4:
        section.index.rename(['facility', 'date', 'analysis', 'type'] , inplace=True)
        section['status'] = 'Followed'
        section = section.set_index('status' , drop = True, append=True, inplace=False)
        section = section.reorder_levels(['facility', 'status', 'date', 'analysis', 'type'])
    section.columns = ['values']
    return section


%%time
table_out = 'start'
for i in range(len(data_to_tab)):
    item = data_to_tab[i]
    date_report = list(item.keys())[0]
    date_analysis = list(item[date_report].keys())[0]
    reports = item[date_report][date_analysis]
    if reports is not None :
        for section_name in list(reports.keys()):
            report_sections = extract_section(reports, section_name)
            if type(table_out) == str:
                table_out = report_sections
            if type(table_out) == pd.core.frame.DataFrame:
                table_out = table_out.append(report_sections)




table_out.to_csv('data/processed/report_trails.csv')
