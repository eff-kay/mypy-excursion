import pandas as pd
import subprocess as sp
import os



def convert_project_names(in_path):
    a = pd.read_csv(open(in_path))
    for filename in os.listdir('repositories'):
        print(f'changing {filename}')
        owners = a[a['project name']==filename]['owner'].values
        owner = owners[0]
        os.rename(f'repositories/{filename}', f'repositories/{owner}-{filename}')

def clone_unique_repos(in_path):
    a = pd.read_csv(open(in_path))
    a_dr = a.drop_duplicates(subset=['owner', 'project name'])
    clone_links = []
    clone_links1 =a[a['project name']=='chainer']['clone_links'].values
    clone_links2 =a[a['project name']=='warehouse']['clone_links'].values
    clone_links = clone_links+list(clone_links1)
    clone_links = clone_links+list(clone_links2)

    print(clone_links)

    os.chdir('repositories')
    for link in clone_links:
        link_sp = link.split('/')
        owner, project_name = link_sp[3], link_sp[4].split('.')[0]
        clone_repo(link, f'{owner}-{project_name}')
    os.chdir('../')

    
def clone_repo(clone_link, folder_name=None):
    print(f'cloning {clone_link}')
    cmd = f'git clone {clone_link} {folder_name}'
    out = sp.run(cmd.split(' '), stdout=sp.PIPE, stderr=sp.PIPE)

    if out.stderr:
        print(f'error while runrning {out.stderr}')
    

    

if __name__=='__main__':
    in_path = 'il_links.csv'
    clone_unique_repos(in_path)
    #convert_project_names(in_path)
    print('done')
