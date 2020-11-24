import pandas as pd
import requests
import os
import json
import pickle
import time

REPOS = os.environ['REPOS']
TYPE_LINES = '../data/combined_type_owner.csv'
NON_TYPE_LINES = '../data/combined_non_type_owner.csv'
TYPE_MAX_PR_PER_PROJECT = 'data/type_max_pr_per_project.csv'
NON_TYPE_MAX_PR_PER_PROJECT = 'data/non_type_max_pr_per_project.csv'
REVIEWER_DB = 'exp_data'
FILE_REVIEWER_DB = 'file_exp_data'

github_api_baseurl= "https://api.github.com"
github_api_graphql = "https://api.github.com/graphql"

headers = {
    'Accept': "application/vnd.github.groot-preview+json",
    'Authorization': "Token 8e1de798669cad2bb25ff213d71d1f849dd2913d",
    'Cache-Control': "ncache",
    'Postman-Token': "a110ce8e-4db8-bb0e-a5bf-a5998a5b0aca"
}


def get_first_n_prs(owner, project):
    query = """query {
repository(owner:"%s", name:"%s"){
    pullRequests(first:100) {
        totalCount
        pageInfo {
            endCursor
            startCursor
        }
        edges{
            node{
                number
                files(first:100){
                    edges{
                        node{
                            path
                        }
                    }
                }
                assignees(last:100){
                    edges{
                        node{
                            login
                            name
                        }
                    }
                }
            }
        }
    }
}
}"""%(owner,project)

    data = {'query':query}

    global github_api_baseurl, headers
    api_url = github_api_graphql 
    res = requests.request('POST', api_url, headers=headers, json=data)

    try:
        json_res = json.loads(res.text)["data"]["repository"]
    except:
        print('request failed trying again', res.status_code, res.text)
        res = requests.request('POST', api_url, headers=headers, json=data)
        json_res = json.loads(res.text)["data"]["repository"]
    return json_res
    #return json_res['pullRequests']["pageInfo"]["endCursor"]
   
def get_next_100(owner,project, end_cursor):
    query = """query {
repository(owner:"%s", name:"%s"){
    pullRequests(first:100, after:"%s") {
        totalCount
        pageInfo {
            endCursor
            startCursor
        }
        edges{
            node{
                number
                files(first:100){
                    edges{
                        node{
                            path
                        }
                    }
                }
                assignees(last:100){
                    edges{
                        node{
                            login
                            name
                        }
                    }
                }
            }
        }
    }
}
}"""%(owner,project, end_cursor)

    data = {'query':query}

    global github_api_baseurl, headers
    api_url = github_api_graphql 
    res = requests.request('POST', api_url, headers=headers, json=data)
    try:
        json_res = json.loads(res.text)["data"]["repository"]
    except:
        print('request failed trying agagin', res.status_code, res.text)
        time.sleep(10)
        res = requests.request('POST', api_url, headers=headers, json=data)
        json_res = json.loads(res.text)["data"]["repository"]

    return json_res

def get_all_project(owner, project, end_cursor=None, last_index=None):
    os.makedirs(f'{FILE_REVIEWER_DB}/{project}', exist_ok=True)
    if end_cursor and last_index:
        print(f'using {end_cursor} and {last_index}')
        i=last_index
        i+=1
        res = get_next_100(owner, project, end_cursor)
    else:
        print('starting from fresh')
        i = 0
        res = get_first_n_prs(owner, project)
    
    res = res['pullRequests']
    json.dump(res, open(f'{FILE_REVIEWER_DB}/{project}/{i}.json', 'w'))
    end_cursor = res['pageInfo']['endCursor']
    edges = res['edges']
    i+=1
    while(len(edges)>0):
        last_max_pr = edges[-1]['node']['number']
        if(project=='ansible' and last_max_pr>=40000):
            print(f'last pr {last_max_pr}')
            break
        print(f'last pr {last_max_pr} {end_cursor} {i-1}')
        res = get_next_100(owner, project, end_cursor)
        res = res['pullRequests']
        json.dump(res, open(f'{FILE_REVIEWER_DB}/{project}/{i}.json', 'w'))
        end_cursor = res['pageInfo']['endCursor']
        edges = res['edges']
        i+=1


def create_reviewerdb_for_all_projects(in_path):
    df = pd.read_csv(in_path)
    endCursor=None
    i=None
    for ind, row in df.iterrows():
        owner = row['owner']
        project_name = row['project name']
        pull_number = row['max_pr']

        if project_name in os.listdir(f'{FILE_REVIEWER_DB}'):
            if project_name=='ansible':
                endCursor="Y3Vyc29yOnYyOpHOCf1PGg=="
                i=196
            else:
                print(f'skipping {project_name}')
                continue
        
        print(f'{project_name} started')
        get_all_project(owner, project_name, end_cursor=endCursor, last_index=i)
        print(f'{project_name} done')

if __name__=='__main__':

    #get_max_pull_number_for_data(TYPE_LINES, TYPE_MAX_PR_PER_PROJECT)
    #next_c = get_first_n_prs("ansible","ansible")
    #get_next_100("ansible","ansible", next_c)
    #get_all_project('ansible', 'ansible')
    create_reviewerdb_for_all_projects(TYPE_MAX_PR_PER_PROJECT)
    print('done')
