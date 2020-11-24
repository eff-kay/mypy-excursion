import os
path = "."

needsColor = True

def diff(folder_name, needColor):
    if needsColor:
        diff_command = 'git diff --color > ../../{}/{}'.format(folder_name, '{}')
    else:
        diff_command = 'git diff > ../../{}/{}'.format(folder_name, '{}')

    folders = [f.name for f in os.scandir(".") if f.is_dir()]
    folders = list(filter(lambda i: str.isnumeric(i), folders))

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    for folder in folders:
        os.chdir(folder)
        git_repo = os.listdir('.')[0]
        os.chdir(git_repo)
        output = '{}.txt'.format(folder)
        os.system(diff_command.format(output))
        os.chdir('../..')

diff('color', True)
diff('no_color', False)