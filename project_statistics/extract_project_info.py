import pandas as pd
import subprocess as sp
import os
from bs4 import BeautifulSoup as bs
import requests
import json
from skipped_repos import skipped


github_api_graphql = "https://api.github.com/graphql"

headers = {
    'Accept': "application/vnd.github.groot-preview+json",
    'Authorization': "Token 8e1de798669cad2bb25ff213d71d1f849dd2913d",
    'Cache-Control': "ncache",
    'Postman-Token': "a110ce8e-4db8-bb0e-a5bf-a5998a5b0aca"
}

def removeNonAscii(s): return "".join(i for i in s if ord(i)<126 and ord(i)>31).strip(' ')

def extract_html(link):
    
    res = requests.request('GET', link)
    
    pv = {}
    if res.status_code==200:
        soup = bs(res.text, 'html.parser')
        container = soup.find_all('div', {'class':'container'})[1]
        div = container.find_all('div', {'class': 'col-md-4'})[1]
        table = div.find_all('table')[0]
        trs = table.find_all('tr')
        for tr in trs:
            tds = tr.find_all('td')
            key = tds[0].text
            #print(tds)
            strong = tds[1].strong
            if strong.a:
                value = strong.a.text
            elif strong.time:
                value = strong.time['title']
            else:
                value = strong.text
            key = removeNonAscii(key)
            value = removeNonAscii(value)
            pv[key] = value
        return pv
    else:
        return None
        #raise Exception('something is wrong', link)

def extract_all_projects(in_path):
    a = pd.read_csv(open(in_path))
    a_dr = a.drop_duplicates(subset=['owner', 'project name'])
    for ind, row in a_dr.iterrows():
        link = 'https://libraries.io/github/'+row['owner']+'/'+row['project name']
        print(link)
        pv = extract_html(link)
        if pv:
            pvdf = pd.DataFrame(pv.items())
            pvdf.to_csv(f'repo_info/{row["owner"]}-{row["project name"]}.csv')
        else:
            skipped.append(link)
            print(f'skip count {len(skipped)}')
        print(f'{ind}, {link} done')
    print(skipped) 


def create_cloc_csv(projects):
    for ind, row in projects.iterrows():
        project_name = row['project name']
        owner = row['owner']
        cmd = f'cloc repositories/{owner}-{project_name} -csv --out=clocs/{owner}_{project_name}.csv'
        out = sp.run(cmd.split(' '), stdout=sp.PIPE, stderr=sp.PIPE)

        #if out.stderr:
        #    if owner=='capitalone':
        #        continue
        #    else:
        #        raise Exception(out.stderr)
        print(f'{ind} done')

def create_cloc_df(projects):
    a={}
    for ind, row in projects.iterrows():
        project_name = row['project name']
        owner = row['owner']
        df = pd.read_csv(open(f'clocs/{owner}_{project_name}.csv'))
        code = df[df['language']=='SUM']['code'].values[0]
        print(code)
        a[f'{owner}-{project_name}'] = code
    
        print(f'{ind} done')
   
    combined_df = pd.DataFrame(a.items())
    combined_df.to_csv('loc_counts.csv')

def get_stars(owner, project):
    query = """query {
    repository(owner:"%s", name:"%s"){
        stargazers{
            totalCount
        }
    }
}"""%(owner,project)

    data = {'query':query}

    global github_api_baseurl, headers
    api_url = github_api_graphql 
    res = requests.request('POST', api_url, headers=headers, json=data)

    try:
        stargazers = json.loads(res.text)["data"]["repository"]['stargazers']['totalCount']
    except:
        print('request failed trying again', res.status_code, res.text)
        res = requests.request('POST', api_url, headers=headers, json=data)
        stargazers = json.loads(res.text)["data"]["repository"]['stargazers']['totalCount']
    return stargazers
    #return json_res[json_res'pullRequests']["pageInfo"]["endCursor"]

def create_stargazer_df(projects):
    a={}
    for ind, row in projects.iterrows():
        project_name = row['project name']
        owner = row['owner']
        #project_name = project.split('/')[-1]
        #owner = project.split('/')[-2]
        stars = get_stars(owner, project_name)
        a[f'{owner}-{project_name}'] = stars
        print(f'{ind} done')
    df = pd.DataFrame(a.items())
    df.to_csv('start_count.csv')

def create_contributor_file(projects):
    for ind, row in projects.iterrows():
        project_name = row['project name']
        owner = row['owner']
        os.chdir(f'repositories/{owner}-{project_name}')
        cmd = 'git log --format="%an"'
        out = sp.run(cmd.split(' '), stdout = sp.PIPE, stderr = sp.PIPE)
        if out.stderr:
            print(out.stderr)
        if out.stdout:
            with open(f'contributor.csv', 'wb') as w:
                w.write(out.stdout)

        print(f'{ind} {project_name} done')
        os.chdir('../../')

def create_contributor_count_df(projects):
    a = {}
    for ind, row in projects.iterrows():
        project_name = row['project name']
        owner = row['owner']
        print(f'{ind} starting, {owner}-{project_name}')
        df = pd.read_csv(open(f'repositories/{owner}-{project_name}/contributor.csv', errors='ignore'), header=None)
        a[f'{owner}-{project_name}'] = len(df[0].unique())


    combined_df = pd.DataFrame(a.items())
    combined_df.to_csv('contributor_count.csv')

if __name__=='__main__':
   #extract_html('https://libraries.io/github/pypa/warehouse')
    
    #skipped = skipped[:1]

    #extract_all_projects('il_links.csv')
    a = pd.read_csv(open('il_links.csv'))
    a_dr = a.drop_duplicates(subset=['owner', 'project name'])
    assert a_dr.shape[0]==211
    a_dr = a_dr[a_dr['owner']!='agrc']
    assert a_dr.shape[0]==210
    #create_cloc_csv(a_dr)
    create_stargazer_df(a_dr)
    #create_contributor_file(a_dr)
    #create_cloc_df(a_dr)
    #create_contributor_count_df(a_dr)
    print('done')
