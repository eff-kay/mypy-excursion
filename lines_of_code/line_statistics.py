import pandas as pd
import os
import subprocess
import pickle

def create_single_pd():
  all_files = os.listdir('csv_files')
  
  stat = {}
  for file in all_files[:]:
    project = file.split(".")[0]
    print("file name {}".format(file))
    a = pd.read_csv('csv_files/'+file)
    stat[project] = {"Python":0, "SUM":0}
   
    python_code = a[a['language']=='Python']['code'] 
    py_count = python_code.iloc[0] if len(python_code)>0 else 0 
    total  = int(a[a['language']=='SUM']['code'])
    stat[project]['Python'] = py_count
    stat[project]['SUM'] = total
    print("{} done", project) 
  final_df = pd.DataFrame(stat)
  with open('test.pickle', 'wb') as w:
    pickle.dump(final_df, w)


if __name__=='__main__':
  print('something')
  
  create_single_pd()
