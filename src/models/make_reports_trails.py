import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import timedelta
import src.models.cohort_analysis_function as caf
from dateutil.relativedelta import relativedelta
import ipyparallel as ipp
import itertools
import importlib



%matplotlib inline

data = pd.read_csv('data/processed/complete_data.csv')

importlib.reload(caf)

def make_dates_sequence(start, end, frequence_analysis='YS'):
    date_reference_list = list(pd.date_range(start=start, end=end, freq='MS'))
    date_analysis_list = list(pd.date_range(start=start, end=end, freq=frequence_analysis))
    combination_list = []
    for date_a in date_reference_list :
        for date_b in date_analysis_list :
            if date_a <= date_b:
                combination_list = combination_list + [[date_a, date_b]]
    return combination_list

analysis_points = make_dates_sequence('2010-01-01', '2012-01-01', frequence_analysis='YS')

%%time
caf.make_report(data, analysis_points[0][0] , analysis_points[0][1],
                        90, 365, 365)


def run_trail(point, data=data):
    reference_date = point[0]
    analysis_date = point[1]
    out = data.groupby('facility').apply(make_report, reference_date, analysis_date, 90, 365, 365)
    return {reference_date:{analysis_date:out}}

rc = ipp.Client()
all_engines = rc[:]
view = rc.load_balanced_view()
import os
%px import os; os.chdir("{os.getcwd()}")

all_engines.push(dict(
    make_report=caf.make_report
))

all_engines.block = True

# TODO only return  data frames. Make counts by facility after that

out = all_engines.map_async(run_trail, analysis_points)
out.wait_interactive(interval = 60)
caf.make_report(data, analysis_points[0][0], analysis_points[0][1], 90, 365, 365)


data.groupby('facility').apply(caf.make_report, analysis_points[0][0], analysis_points[0][1], 90, 365, 365)

analysis_points[0]
r

un_trail(analysis_points[0])

a = out.get()

out.get()




pd.DataFrame.from_list(a)
