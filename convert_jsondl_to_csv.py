import newlinejson as nlj
import json,csv

d = []

with nlj.open('corpus_jsondl.json') as src:
    for line in src:
        d.append(line)

    field_names  = list(d[0].keys())

    csv_file = open("out.csv", 'w')
    for item in d:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writerow(item)
        

    
