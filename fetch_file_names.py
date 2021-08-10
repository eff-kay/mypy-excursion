import requests
import fnmatch
import json

github_api_baseurl= "https://api.github.com"

def get_file_names(pull_request_url):
    spliturl = pull_request_url.split("/")
    owner, repo, pull_number = spliturl[3], spliturl[4], spliturl[6]
    api_url = github_api_baseurl+"/repos/{}/{}/pulls/{}/files".format(owner,repo,pull_number)
    response = requests.request("GET", api_url, headers=headers)
    file_names = [modification["filename"].split("/")[-1] for modification in response.json()]
    filtered_files = fnmatch.filter(file_names, "*.py")
    return True if len(filtered_files)>0 else False

if __name__ == "__main__":
    jsonFile = open('july_pull_requests.json')
    jsonData = json.load(jsonFile)
    updatedJsonData = json.load(open('july_pull_requests_python_files.json'))
    for i, item in enumerate(jsonData):
        if(get_file_names(item['pull_url'])):
            updatedJsonData.append(item)
        print('index {} done {}'.format(i, item['pull_url']))
    with open('july_pull_requests_python_files.json', 'w') as w:
        json.dump (updatedJsonData, w) 

    # print(get_file_names("https://github.com/chap/damn-menu/pull/2"))


    