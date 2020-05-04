from unique_projects import a
import subprocess


def create_cloc(project):
  project_link = 'https://github.com/'+project+'.git'
  cmd  = "git clone --depth 1 "+project_link
  subprocess.run(cmd.split(" "))
  folder_name = project.split("/")[1] 
  cmd = "cloc "+folder_name+" --report-file cloc_files/"+folder_name+".cloc"
  subprocess.run(cmd.split(" "))



for i, project in enumerate(a[:], 0):
  create_cloc(project)
  print(str(i)+" done")
  cmd = "rm -rf "+project.split("/")[1]
  subprocess.run(cmd.split(' '))





  
