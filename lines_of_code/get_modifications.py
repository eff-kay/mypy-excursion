import requests
from bs4 import BeautifulSoup
import json
import pull_request_info
import pickle
import pandas as pd
import subprocess
import os

def check_for_fixed_by(url):
    resp = requests.request("GET", url)
    source = resp.text
    tokenized_source = BeautifulSoup(source, 'html.parser')
    span = tokenized_source.find('div', {"class": "css-truncate my-1"})
    if span:
        try:
            href = BeautifulSoup(str(span), 'html.parser').a['href']
            print('found', href)
            return href
        except:
            return None        
    else:
        return span

def get_modifications():
    urls  = open('sample_urls.txt').read().split('\n')
    pull_diff = []
    for i, url in enumerate(urls[:]):
      if len(pull_diff)==400:
        break
      pull_url = check_for_fixed_by(url)
      print(pull_url)
      if(pull_url):
        commits, add, dels = pull_request_info.get_add_sub(pull_url)
        pull_diff.append((commits, add, dels))
      print("{} done".format(i))
    with open("pull_request.pickle", 'wb') as w:
        df = pd.DataFrame(pull_diff)
        df.columns = ['commits', 'adds', 'subs']
        pickle.dump(df, w)


def get_commits():
    urls  = open('sample_urls.txt').read().split('\n')
    pull_diff = []
    for i, url in enumerate(urls[:]):
      if len(pull_diff)==400:
        break
      pull_url = check_for_fixed_by(url)
      print(pull_url)
      if(pull_url):
        commit= pull_request_info.get_commit_sha(pull_url)
        pull_diff.append(commit)
      print("{} done".format(i))
    with open("commits.p", 'wb') as w:
        df = pd.DataFrame(pull_diff)
        df.columns = ['commits']
        pickle.dump(df, w)

def create_cloc():
    ucommits  = pickle.load(open('urls_pullcommits.p', 'rb'))

    for i, (commit, url) in enumerate(ucommits[:2].values):
      spliturl = url.split("/")
      owner, repo, issue_number = spliturl[3], spliturl[4], spliturl[-1]
      project = owner + "/"+repo 
      project_link = 'https://github.com/'+project+'.git'

      cmd  = "git clone --depth 1 "+project_link
      subprocess.run(cmd.split(" "))

      folder_name = project.split("/")[1]

      os.chdir(folder_name)

      cmd = "git checkout "+commit
      subprocess.run(cmd.split(" "))

      os.chdir("..")
      
      cmd = "cloc "+folder_name+" --csv --report-file cloc_issue_files/"+folder_name+"_"+commit+".csv"
      subprocess.run(cmd.split(" "))

      cmd = "rm -rf "+folder_name 
      subprocess.run(cmd.split(" "))

      
      print("{} done".format(i))
    
        
  
if __name__ == "__main__":
    #issues  = json.load(open('../src/entire_corpus_python_patches/0.json'))
    #pull_diff = []
    #for i, item in enumerate(issues[:2]):
    #  if len(pull_diff)==400:
    #    break
    #  pull_url = check_for_fixed_by(item['url'][1:-1])
    #  print(pull_url)
    #  if(pull_url):
    #    commits, add, dels = pull_request_info.get_add_sub(pull_url)
    #    pull_diff.append((commits, add, dels))
    #  print("{} done".format(i))
    #  
    #with open("pull_request.pickle", 'wb') as w:
    #    pickle.dump(pull_diff, w)
    #issue_url = issues[0]['url'][1:-1]
    #print(issue_url)
    #print(check_for_fixed_by(issue_url))
    #print(get_commits())
    print(create_cloc())
