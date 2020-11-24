import pandas as pd
import requests
import os
import json
import pickle
from reviewer_utils import get_pull_request_for_commit
from glob import glob

REPOS = os.environ['REPOS']
TYPE_LINES = '../data/combined_type_owner1.csv'
NON_TYPE_LINES = '../data/combined_non_type_owner.csv'
TYPE_MAX_PR_PER_PROJECT = 'data/type_max_pr_per_project.csv'
NON_TYPE_MAX_PR_PER_PROJECT = 'data/non_type_max_pr_per_project.csv'

TYPE_REVIEW_EXP= 'data/review_count_type1.csv'
NON_TYPE_REVIEW_EXP = 'data/review_count_non_type.csv'

REVIEWER_DB = 'exp_data'


github_api_baseurl= "https://api.github.com"
github_api_graphql = "https://api.github.com/graphql"

headers = {
    'Accept': "application/vnd.github.groot-preview+json",
    'Authorization': "Token 8e1de798669cad2bb25ff213d71d1f849dd2913d",
    'Cache-Control': "ncache",
    'Postman-Token': "a110ce8e-4db8-bb0e-a5bf-a5998a5b0aca"
}

def create_csvs_from_reviewer_db(project_name):
    dfs=[]
    for json_file in glob(f'{REVIEWER_DB}/{project_name}/*.json'):
        new_json = {}
        json_data  = json.load(open(f'{json_file}'))
        for edge in json_data['edges']:
            pull_no = edge['node']['number']
            for assignee in edge['node']['assignees']['edges']:
                if assignee['node']['name']:
                    new_json[assignee['node']['name']] = pull_no
                    print(f'{pull_no} has a name')
                else:
                    new_json[assignee['node']['login']] = pull_no
                    print(f'{pull_no} has no name but a login')
        
        if new_json:
            df = pd.DataFrame(new_json.items())
            print(df.head())
            df.columns=['authors','pull_no']
            dfs.append(df)
   
    combined_df = pd.concat([df for df in dfs])
    combined_df.reset_index(inplace=True, drop=True)
    combined_df = combined_df.sort_values(by='pull_no')
    combined_df.to_csv(f'{REVIEWER_DB}/{project_name}/{project_name}.csv')
    print('file created')

def convert_all_reviewer_dbs(in_path):
    df = pd.read_csv(in_path)
    for ind, row in df.iterrows():
        owner = row['owner']
        project_name = row['project name']
        pull_number = row['max_pr']

        if len(glob(f'{REVIEWER_DB}/{project_name}/{project_name}.csv'))>0:
            continue
        print(f'starting {project_name}')
        create_csvs_from_reviewer_db(project_name)
        print(f'{project_name} done')

def count_reviewer_exp(in_file, out_file):
    df = pd.read_csv(open(in_file))
    df['reviewer_count'] = 0
    for ind, row in df.iterrows():
        owner = row.owner
        project_name = row['project name']
        commit_id = row['bug_inducing_commit']
        author = row['buggy author']
        pr = get_pull_request_for_commit(owner, project_name, commit_id)
        if len(pr)==0:    
            print(f'skipping {project_name} {commit_id}')
            continue

        project_db = pd.read_csv(open(f'{REVIEWER_DB}/{project_name}/{project_name}.csv'))
        pull_no = int(pr['number'])
        exp_count = project_db[project_db.pull_no<pull_no].authors.value_counts().get(author)
        if exp_count:
            df.loc[ind, ['reviewer_count']] = exp_count
        print(f'{pull_no} {author} {project_name} {commit_id} {exp_count} done') 
    df.to_csv(out_file)

if __name__=='__main__':

    #create_csvs_from_reviewer_db('ansible')
    #convert_all_reviewer_dbs(TYPE_MAX_PR_PER_PROJECT)
    #convert_all_reviewer_dbs(NON_TYPE_MAX_PR_PER_PROJECT)

    #count_reviewer_exp(NON_TYPE_LINES,NON_TYPE_REVIEW_EXP)
    count_reviewer_exp(TYPE_LINES,TYPE_REVIEW_EXP)
    print('done')
