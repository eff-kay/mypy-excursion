import json


jsonD = json.load(open('entire_corpus.json'))
unit = 37374

for i in range(10):
    json_temp = jsonD[i*unit:unit*(i+1)]
    if i==9:
        json_temp.append(jsonD[373740])
        json_temp.append(jsonD[373741])

    json_file = open('entire_corpus/entire_corpus_'+str(i)+".json", 'w')
    json.dump(json_temp, json_file)


