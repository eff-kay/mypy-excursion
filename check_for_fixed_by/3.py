import requests
from bs4 import BeautifulSoup
import json
import fetch_file_names

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
    jsonFile = open('../entire_corpus/entire_corpus_3.json')
    jsonData = json.load(jsonFile)
    updatedJsonData = json.load(open('../entire_corpus_python_patches/3.json'))
    for i, item in enumerate(jsonData):
        if(len(updatedJsonData)<373742):
            pull_url = check_for_fixed_by(item['url'][1:-1])
            if(pull_url):
                if(fetch_file_names.get_file_names(pull_url)):
                    updatedJsonData.append(item)
            print('index {} done {}, count {}'.format(i, item['url'], len(updatedJsonData)))
        else:
            break
    with open('../entire_corpus_python_patches/3.json', 'w') as w:
        json.dump(updatedJsonData, w) 