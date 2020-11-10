import pandas as pd
import os
import subprocess

def convert_files_to_csv():
  all_files = os.listdir('cloc_files')
  for i, file in enumerate(all_files[:], 0):
    print(file)
    cmd = "cloc cloc_files/"+file+" --csv --sum-reports --report-file csv_files/" +file.split(".")[0]+".csv"
    print(cmd.split(" "))
    subprocess.run(cmd.split(" "))
    print("{} done".format(i))


def create_single_pd():
  all_files = os.listdir('cloc_files')
  
  stat = {}
  for file in all_files[:2]:
    project = file.split(".")[0]
    print("file name {}".format(file))
    a = pd.read_csv('cloc_files/'+file)
    print(a.head())
    #stat[project] = {}
    #py_count = a[a['language']=='Python']
    #total  = a[a['SUM']=='Python']
    #stat[project]['Python'] = py_count
    #stat[project]['SUM'] = total
  
  final_df = pd.DataFrame(stat)
  print(final_df)


if __name__=='__main__':
  print('something')
  convert_files_to_csv()
