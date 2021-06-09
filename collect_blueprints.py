import os
import pandas as pd
import re
import shutil

from pydriller.repository import Repository, Git


def get_files(path_to_repo: str) -> set:
    """ Return all the files in the repository
    Return
    ------
    set[str]
        The set of filepath relative to the root of repository
    """

    files = set()

    for root, _, filenames in os.walk(path_to_repo):
        if '.git' in root:
            continue
        for filename in filenames:
            path = os.path.join(root, filename)
            path = path.replace(path_to_repo, '')
            if path.startswith('/'):
                path = path[1:]

            files.add(path)

    return files


repos = pd.read_csv(os.path.join('data', 'tosca_repositories.csv'))
blueprints = pd.DataFrame(columns=['repo_id', 'url'])

i = 0
for _, row in repos.iterrows():
    i += 1

    print(f'({i}/{repos.shape[0]}) Collecting data from', row['full_name'])

    path_to_remote_repo = f'https://github.com/{row["full_name"]}'
    path_to_local_repo = os.path.join('/tmp/', row["full_name"].split('/')[1])

    try:
        releases = list(commit for commit in Repository(path_to_repo=path_to_remote_repo,
                                                        only_releases=True,
                                                        order='date-order',
                                                        clone_repo_to='/tmp/').traverse_commits())

        if releases:
            # Get the most recent release
            latest_release_hash = releases[-1].hash

            git_repo = Git(path_to_local_repo)
            git_repo.checkout(latest_release_hash)

            for filepath in get_files(path_to_local_repo):

                if 'test' in filepath:
                    # Ignore files used for test
                    continue

                _, extension = os.path.splitext(filepath)

                if extension == '.tosca':
                    blueprints = blueprints.append({
                        'repo_id': row['id'],
                        'url': f'https://raw.githubusercontent.com/{row["full_name"]}/{latest_release_hash}/{filepath}'
                    }, ignore_index=True)

                elif extension in ('.yml', '.yaml'):
                    # Read the file content to check if tosca_definitions in file
                    try:
                        with open(os.path.join(path_to_local_repo, filepath), 'r') as f:
                            if re.match(r'^tosca_definitions_version\s*:.+', f.read()):
                                blueprints = blueprints.append({
                                    'repo_id': row['id'],
                                    'url': f'https://raw.githubusercontent.com/{row["full_name"]}/{latest_release_hash}/{filepath}'
                                }, ignore_index=True)
                    except UnicodeDecodeError:
                        continue

        blueprints.to_csv(os.path.join('data', 'tosca_blueprints.csv'), index=False)

    except Exception as e:
        print(e)

    finally:
        if os.path.isdir(path_to_local_repo):
            shutil.rmtree(path_to_local_repo)
