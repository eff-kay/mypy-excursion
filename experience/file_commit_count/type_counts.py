import pandas as pd
import subprocess as sp
import os
from io import StringIO, BytesIO

TYPE_CSV = '../data/combined_type.csv'
NON_TYPE_CSV = '../data/combined_non_type.csv'
REPOS = os.environ['REPOS']

def get_author_count(commit, filename, buggy_author, project_path):
    print(f'running exp count for {buggy_author} {project_path}')
    os.chdir(f'{project_path}')
    command = f"git log {commit} --format='%aN,%H' --follow -- {filename}"

    result = sp.run(command.split(' '), stdout=sp.PIPE, stderr=sp.PIPE)
    if result.stderr:
        raise Exception(f'some error {result.stderr}')
    if result.stdout:
        result = BytesIO(result.stdout)
        au_exp = pd.read_csv(result,header=None)
        au_exp.columns = ['author', 'commit']
        au_exp.author = au_exp.author.apply(lambda x: x.strip("'"))
        au_exp = au_exp[au_exp.author==buggy_author]
        return au_exp.shape[0]-1
    else:
        return 0

def count_type_exp(type_csv, dest):
    type_commits = pd.read_csv(type_csv)

    type_commits = type_commits[['filename','bug_inducing_commit', 'buggy author', 'id', 'directory', 'project name']]
    
    workdir = os.getcwd()
    exp_counts = []
    for ind, commit in type_commits.iterrows():
        print(commit)
        os.chdir(REPOS)
        exp_count = get_author_count(commit['bug_inducing_commit'], commit['filename'], commit['buggy author'], commit['directory'])
        exp_counts.append(exp_count)
    type_commits['file_exp'] = pd.Series(exp_counts+[0]*(type_commits.shape[0]-1))
    os.chdir(workdir)
    type_commits.to_csv(dest)

def count_non_type_csv(non_type_csv, dest):
    type_commits = pd.read_csv(non_type_csv)

    type_commits = type_commits[['filename_x','bug_inducing_commit', 'buggy author', 'id', 'directory', 'project name']]
    
    workdir = os.getcwd()
    exp_counts = []
    for ind, commit in type_commits.iterrows():
        print(commit)
        os.chdir(REPOS)
        exp_count = get_author_count(commit['bug_inducing_commit'], commit['filename_x'], commit['buggy author'], commit['directory'])
        exp_counts.append(exp_count)
    type_commits['file_exp'] = pd.Series(exp_counts+[0]*(type_commits.shape[0]-1))
    os.chdir(workdir)
    type_commits.to_csv(dest)



if  __name__=='__main__':
    count_non_type_csv(NON_TYPE_CSV, 'file_exp_non_type.csv')
    print('done')
