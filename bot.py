import subprocess
from git import Repo

filename = 'main.py'
while True:
    # Clone from github repo
    Repo.clone_from('git@github.com:Gamefist/ScrappyBot.git', 'ScrappyBot')

    # Open subprocess and .wait() for it to close or kill
    p = subprocess.Popen('python ' + filename, shell=True).wait()

    # Loop repeats when there is an error, else it exits the loop
    if p != 0:
        continue
    else:
        break
