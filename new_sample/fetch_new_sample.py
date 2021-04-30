import json
import random

CORPUS_LOCATION = '../entire_corpus_python_patches'



full_corpus = []

for i in range(10):
    full_corpus.extend(json.load(open(f'{CORPUS_LOCATION}/{i}.json')))


full_corpus_links = [x['url'].replace('"','') for x in full_corpus]
assert len(full_corpus_links)==10916, f'the existing corpus was 10916'


sample_links = open('main_sample.txt').read().split()
assert len(sample_links) == 400, f'the sample size was 400'


new_sample = []

temp_corpus = list(full_corpus_links)
random.shuffle(full_corpus_links)

assert temp_corpus != full_corpus_links, 'they should not be equal after the shuffle'


for x in full_corpus_links:
    if x not in new_sample and x not in sample_links:
        new_sample.append(x)

# this number was manually verified
assert len(new_sample)==10021, 'this should be equal to 10021'

with open('remaining_corpus.txt', 'w') as w:
    for x in new_sample:
        w.write(x)
        w.write('\n')
    w.close()