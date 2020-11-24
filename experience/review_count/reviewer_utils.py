import pandas as pd
import requests
import os

REPOS = os.environ['REPOS']
TYPE_LINES = '../data/combined_type_owner.csv'
NON_TYPE_LINES = '../data/combined_non_type_owner.csv'
TYPE_MAX_PR_PER_PROJECT = 'data/type_max_pr_per_project.csv'
NON_TYPE_MAX_PR_PER_PROJECT = 'data/non_type_max_pr_per_project.csv'

github_api_baseurl= "https://api.github.com"
headers = {
    'Accept': "application/vnd.github.groot-preview+json",
    'Authorization': "Token 8e1de798669cad2bb25ff213d71d1f849dd2913d",
    'Cache-Control': "ncache",
    'Postman-Token': "a110ce8e-4db8-bb0e-a5bf-a5998a5b0aca"
}

def get_pull_request_for_commit(owner,project_name, commit_id):
    global github_api_baseurl, headers
    api_url = github_api_baseurl + f'/repos/{owner}/{project_name}/commits/{commit_id}/pulls'
    res = requests.request('GET', api_url, headers=headers)
    rjson = res.json()
    if len(rjson)>1:
        rjson = sorted(rjson, key=lambda x:x.get('number'), reverse=True)
        rjson = rjson[0]
    elif len(rjson)==0:
        return [] 
    else:
        rjson= rjson[0]
    
    return rjson


def get_reviewer_name(login):
    api_url = github_api_baseurl + f'/users/{login}'
    res = requests.request('GET', api_url, headers=headers)
    rjson = res.json()
    if rjson=={}:
        raise Exception('provide a valid login')
    else:
        return rjson.get('name') if rjson.get('name')!=None else login

def get_reviewer_names(owner, project_name, pull_number):
    api_url = github_api_baseurl + f'/repos/{owner}/{project_name}/pulls/{pull_number}'
    print(f'{api_url}')
    res = requests.request('GET', api_url, headers=headers)
    
    pr = res.json()
    if pr.get('message')!="Not Found":
        assignees = list(map(lambda x: x.get('login'), pr.get('assignees', [])))
        reviewers = list(map(lambda x: x.get('login'), pr.get('requested_reviewers', [])))
        rlist = set(assignees+reviewers)
        #print(f'rlist {rlist}') 
        rnames = [get_reviewer_name(login) for login in rlist]
        #print(f'rname = {rnames}')
        return rnames
    else:
        print('no pr')
        return []


def create_project_reviewer_db(owner,  project_name, pull_number):
    number = pull_number
    pr_exp = []
    lower_bound = 0
    #if project_name=='ansible':
    #    lower_bound = 31280
    #if project_name=='blaze':
    #    lower_bound = 1000
    #if project_name=='manticore':
    #    lower_bound = 700
    #if project_name=='astrophy':
    #    lower_bound = 7800
     
    while(number>lower_bound):
        rnames = get_reviewer_names(owner, project_name, number)
        for name in rnames:
            pr_exp.append({'pr':number, 'author':name})
        number-=1
    pr_exp_df = pd.DataFrame(pr_exp)
    pr_exp_df.pr = pr_exp_df.pr.astype('int')
    pr_exp_df.to_csv(f'exp_data/{project_name}.csv')
    print(f'{project_name} done')

def create_reviewerdb_for_all_projects(in_path):
    df = pd.read_csv(in_path)
    for ind, row in df.iterrows():
        owner = row['owner']
        project_name = row['project name']
        pull_number = row['max_pr']

        create_project_reviewer_db(owner, project_name, pull_number)
        print(f'{project_name} done')

def get_max_pull_number_for_data(in_path, to_path):
    df = pd.read_csv(in_path)
    project_pr = {}
    owner_project_map ={}
    for ind, row in df.iterrows():
        owner = row.owner
        project_name = row['project name']
        commit_id = row['bug_inducing_commit']
        author = row['buggy author']
        pr = get_pull_request_for_commit(owner, project_name, commit_id)
        if len(pr)==0:    
            print(f'skipping {project_name} {commit_id}')
            continue
        if project_name in project_pr:
            if project_pr[project_name]<pr['number']:
                project_pr[project_name] = pr['number']
        else:
            owner_project_map[project_name] = owner
            project_pr[project_name] = pr['number']
        print(f'{ind} {project_name} {pr["number"]} done')
    pro_pr_df = pd.DataFrame(project_pr.items()) 
    pro_pr_df.columns = ['project name', 'max_pr']
    owner_project_df = pd.DataFrame(owner_project_map.items()) 
    owner_project_df.columns = ['project name', 'owner']
    print(owner_project_df)
    pro_pr_df = pd.merge(pro_pr_df, owner_project_df, on=['project name'], how='left')
    pro_pr_df['max_pr'] = pro_pr_df['max_pr'].astype('int')
    #pro_pr_df = pro_pr_df[['owner', 'project name', 'max_pr', 'issue id']]
    pro_pr_df.to_csv(to_path)

def get_review_exp(owner, project_name, commit_id, author):
    pr = get_pull_request_for_commit(owner, project_name, commit_id)
    rcount=0
    pr_exp = []
    last_max_pr = 20000
    pr_exp_df_old= None
    if len(pr)!=0:
        number = int(pr['number'])
        # check if the project already exist
        if f'{project_name}.csv' in os.listdir('exp_data'):
            # check if the last max pr was higher than the current one
            pritn('file exists')
            pr_exp_df_old = pd.from_csv(open(f'exp_data/{project_name}.csv'))
            last_pr = pr_exp_df_old.pr.max()
            if number <=last_pr:
                # return the last exp
                rcount = pr_exp_df_old[pr_exp_df_old.pr<=number].exp.values[0]
                return rcount
            # else set the end point to the last max pr
            else:
                last_max_pr = pr_exp_df_old.pr.values[0]
                rcount = pr_exp_df_old.exp.values[0]
        else: 
            print('starting a new project')
        while(number>last_max_pr):
            rnames = get_reviewer_names(number)

            if author in rnames:
                rcount+=1
            
            pr_exp.append({'pr':number, 'exp':rcount})
            number-=1
            print(f'review count {rcount}')
        pr_exp_df = pd.DataFrame(pr_exp)
        pr_exp_df.exp = pr_exp_df.exp.astype('int')
        pr_exp_df.pr = pr_exp_df.pr.astype('int')
        pr_exp_df.exp = rcount - pr_exp_df.exp
        if pr_exp_df_old!=None:
            pr_exp_df = pd.concat([pr_exp_df_old, pr_exp_df]).sort_values(by='pr', ascending=False)
            pr_exp_df.reset_index(drop=True, inplace=True)
        pr_exp_df.to_csv(f'exp_data/{project_name}.csv')
        return rcount
    else:
        return rcount
    
    #print(f'rcount so far {rcount}')

if __name__=='__main__':
   # df = pd.read_csv(TYPE_LINES) 
   # owner = df.iloc[0].owner
   # project_name = df.iloc[0]['project name']
   # commit_id = df.iloc[0]['bug_inducing_commit']
   # author = df.iloc[0]['buggy author']
   # print(f'{df.iloc[0]}')
   # rjson = get_review_exp(owner, project_name, commit_id, author) 

    get_max_pull_number_for_data(NON_TYPE_LINES, NON_TYPE_MAX_PR_PER_PROJECT)
    #create_reviewerdb_for_all_projects(TYPE_MAX_PR_PER_PROJECT)
    print('done')
