import os
from pathlib import Path

from github import Github
import pandas as pd
from datetime import datetime as dt


def run_each_repo(username, token, reponame, save_csv=True):
    if save_csv:
        os.system(f'gts {username}:{token} {reponame}')
    else:
        os.system(f'gts {username}:{token} {reponame} no_csv')


def get_top_paths(username: str, token: str, reponame: str,
                  save_csv: bool = True):

    now = dt.now()

    g = Github(token)
    repo = g.get_repo(f"{username}/{reponame}")
    top_path_list = repo.get_top_paths()
    result = [p.raw_data for p in top_path_list]
    df = pd.DataFrame.from_records(result)
    df.insert(loc=0, column='date', value=now.strftime('%Y-%m-%d'))

    if save_csv:
        outfile = f"{now.strftime('%Y-%m-%d-%Hh-%Mm')}-paths-stats.csv"
        path = Path(outfile)
        if not path.exists:
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', index=False, header=False)
