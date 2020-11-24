from GitCommander import GitCommander
import pandas as pd
import os
import subprocess

import subprocess
import os
import pandas as pd
from functools import reduce
from dateutil.relativedelta import relativedelta
from datetime import datetime
from tqdm.notebook import tqdm
import cliffsDelta

def create_type_df(repodir):
    #working_directory = 'C:/Users/chenp/Documents/Mypy-Labelling/'
    #os.chdir(repodir)
    defects_info = pd.read_csv('defect_authoring.csv')
    defects_info['directory'] = defects_info['directory'].apply(lambda li: f'{repodir}/{li}')
    cwd = os.getcwd()

    stats = pd.DataFrame([], columns = ['line number', 'filename', 'commit id','issue id', 'buggy commit', 'buggy author', 'author experience', 'project progress', 'timedelta (month)'])
    for index, defect in defects_info.iterrows():
        print(f'conducting analysis on {defect} at {index}')
        os.chdir(defect['directory'])
        lines = defect['type error lines'].split(', ')

        for line in lines:
            row = process_defect(defect['buggy commit'], defect['file path'], line, line)
            row.insert(0, line)
            row.insert(1, defect['file path'])
            row.insert(2, defect['buggy commit'])
            row.insert(3, defect['issue id'])
            stats.loc[0 if pd.isnull(stats.index.max()) else stats.index.max() + 1] = row
        os.chdir(cwd)
    stats.to_csv('type.csv')

if __name__=='__main__':
    repodir = os.environ['REPOS']
    print('REPODIR', repodir)
    create_type_df(repodir)

