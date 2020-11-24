import subprocess
from functools import reduce
class GitCommander:
    SAVE_CURRENT_WORKING_DIRECTORY = 'CURR_DIR=$PWD'
    GO_BACK_TO_WORKING_DIRECTORY = 'cd $CURR_DIR'

    GIT_LOG = "git log --format='%H;%at'"

    def getHead(self):
        return subprocess.check_output(
        f'git rev-parse HEAD',
        shell=True).decode('utf-8')

    def checkout(self, commit):
        checkoutCommand = "git checkout "+commit

        return subprocess.check_output(
        checkoutCommand,
        shell=True).decode('utf-8')


    def gitBlame(self, file, startLine, endLine, commit = None):
        if commit:
            blameCommand = "git blame {} -p {} -L {},{}".format(commit, file, startLine, endLine)
        else:
            blameCommand = "git blame -p {} -L {},{}".format(file, startLine, endLine)

        blameText = subprocess.check_output(
        blameCommand,
        shell=True).decode('utf-8')

        if blameText.count('\n') <= 1:
            return None
        else:
            return blameText

    def getModifiedLinesFromGitDiff(self, headCommit, commitToCompare):
        diffCommand = "git diff {} {} -U0 | grep -Po '^--- ./\K.*|^@@ -\K[0-9]+(,[0-9]+)?(?= \+[0-9]+(,[0-9]+)? @@)'".format(headCommit, commitToCompare)

        diffText = subprocess.check_output(
        diffCommand,
        shell=True).decode('utf-8')

        return diffText

    def gitLogInline(self, commit = 'HEAD', author = None):
        if author:
            logCommand = 'git log {} --author="{}" --format="%H;%s;%an;%ct"'.format(commit, author)
        else:
            logCommand = 'git log {} --format="%H;%s;%an;%ct"'.format(commit)

        logText = subprocess.check_output(
        logCommand,
        shell=True).decode('latin-1')
        return logText.split('\n')[:-1] # will always have an empty line at the end of the output

    def parseGitBlame(self, text):
        returnHash = {}
        splitText = text.split("\n")
        firstLine = splitText[0]
        commitId = firstLine.split(" ")[0]
        secondLine = splitText[1]
        authorName = secondLine.split(" ")[1:]
        fullname = reduce(lambda a, b: a + ' ' + b, authorName)
        return [fullname, commitId]
