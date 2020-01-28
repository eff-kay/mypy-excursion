import json


jsonD = []
for i in range(10):
    if i==0:
        json_temp = json.load(open('entire_corpus/entire_corpus_'+str(i)+'.json'))
        first_two = json_temp[:2]

    if i==9:
        json_temp = json.load(open('entire_corpus/entire_corpus_'+str(i)+'.json'))
        last_three = json_temp[-3:]

    jsonD += json.load(open('entire_corpus/entire_corpus_'+str(i)+'.json'))

entire_corpus_d = json.load(open('entire_corpus.json'))
original_first_two = entire_corpus_d[:2]
original_last_three = entire_corpus_d[-3:]

print("verify length: ", len(jsonD)==len(entire_corpus_d), "\n verify first two:", original_first_two==first_two, "\n verify last three: ", original_last_three==last_three)