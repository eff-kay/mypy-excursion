import requests
from bs4 import BeautifulSoup
import json

def check_for_fixed_by(url):
    resp = requests.request("GET", url)
    source = resp.text
    tokenized_source = BeautifulSoup(source, 'html.parser')
    span = tokenized_source.find('span', {"class": "js-enable-hovercard"})
    if span:
        try:
            href = BeautifulSoup(str(span), 'html.parser').span.span.span.a['href']
            print('found', href)
            return href
        except:
            return None        
    else:
        return span


if __name__ == "__main__":
    jsonFile = open('july_issues_closed.json')
    jsonData = json.load(jsonFile)
    updatedJsonData = json.load(open('july_issues_closed_with_prs.json'))
    for i, item in enumerate(jsonData):
        if(check_for_fixed_by(item['url'][1:-1])):
            updatedJsonData.append(item)
        print('index {} done {}'.format(i, item['url']))
    with open('july_issues_closed_with_prs.json', 'w') as w:
        json.dump(updatedJsonData, w) 