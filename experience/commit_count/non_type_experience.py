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
from utils import process_defect

def get_line_changes_for_py_files(lines):
    lineMap = {}
    # go over the commit change to record all the lines change for python files
    i = 0
    lineCount = 0
    while i < len(lines):
        while i < len(lines) and '.py' not in lines[i]:
            i += 1

        if i >= len(lines): break

        filename = lines[i]
        lineMap[filename] = []
        i += 1

        while i < len(lines):
            if lines[i].isdigit():
                lineMap[filename].append(int(lines[i]))
                lineCount += 1
            elif ',' in lines[i]:
                line = lines[i].split(',')
                start = int(line[0])
                count = int(line[1])
                for j in range(0, count):
                    lineMap[filename].append(start + j)
                    lineCount += 1
            else:
                break
        i += 1
    return (lineMap, lineCount)

def get_blame_stats(commit, lineMap, count=0):
    stats = []

    if count > 0:
        pBar = tqdm(total = count, leave=False)

    for key in lineMap:
        for line in lineMap[key]:
            # ignore type-related lines
            if '{}{}{}'.format(line, key, commit) not in typeLineSet:
                row = process_defect(commit, key, line, line)
                row = [line, key, commit] + row
                stats.append(row)
            if count > 0:
                pBar.update(1)

    if count > 0:
        pBar.close()

    return stats

def process_commit_blame(defect):
    cwd = os.getcwd()
    os.chdir(cwd)
    os.chdir(defect['directory'])
    headCommit = defect['buggy commit']
    commitToCompare = defect['fix commit']
    diffCommand = "git diff {} {} -U0 | grep -Po '^--- ./\K.*|^@@ -\K[0-9]+(,[0-9]+)?(?= \+[0-9]+(,[0-9]+)? @@)'".format(headCommit, commitToCompare)

    # execute the diff command with grep pattern matching in a spawned child bash shell for windows
    with subprocess.Popen(['sh'],stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True) as process:
        output = process.communicate(diffCommand.encode())[0].decode('utf-8')

    output = output.split('\n')
    (lineMap, count) = get_line_changes_for_py_files(output)
    authorStats = get_blame_stats(headCommit, lineMap, count)

    os.chdir(cwd)
    return authorStats


def create_nontype_df(repodir):
    defects_info = pd.read_csv('defect_authoring.csv')
    defects_info['directory'] = defects_info['directory'].apply(lambda li: f'{repodir}/{li}')
    cwd = os.getcwd()

    idSet = set()
    nonTypeStats = pd.DataFrame([], columns = ['line number', 'filename', 'commit id', 'buggy commit', 'buggy author', 'author experience', 'project progress', 'timedelta (month)'])

    pBar = tqdm(total=defects_info.shape[0], leave=False)
    for index, defect in defects_info.iterrows():
        print(f'conducting analysis on {index} {defect}')
        if defect['id'] not in idSet:
            rows = process_commit_blame(defect)
            for row in rows:
                print(f'analysizing {row}')
                nonTypeStats.loc[0 if pd.isnull(nonTypeStats.index.max()) else nonTypeStats.index.max() + 1] = row
            idSet.add(defect['id'])
        pBar.update(1)
    nonTypeStats.to_csv('non_type.csv')


if __name__=='__main__':
    repodir = os.environ['REPOS']
    print('REPODIR', repodir)
    create_nontype_df(repodir)
