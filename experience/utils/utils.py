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

def timeDeltaMonth(time1, time2):
    time1 = datetime.fromtimestamp(time1)
    time2 = datetime.fromtimestamp(time2)
    delta = relativedelta(time2, time1)
    return delta.years * 12 + delta.months


# Assume the working directory is already switched to the required working directory
def process_defect(commit, file, start_line, end_line):
    commander = GitCommander()
    blame = commander.parseGitBlame(commander.gitBlame(file, start_line, end_line, commit))
    blame_author = blame[0]
    blame_commit = blame[1] #use the full commit id
    author_commits = commander.gitLogInline(blame_commit, blame_author)

    type_err_commit = author_commits[0].split(';')
    first_commit = author_commits[-1].split(';')
    formatted_time = timeDeltaMonth(int(first_commit[-1]), int(type_err_commit[-1]))
    repo_commits = commander.gitLogInline(blame_commit)

    # length -1 to exclude the most recent type error commit
    return [blame_commit, blame_author, len(author_commits) - 1, len(repo_commits) - 1, formatted_time]

