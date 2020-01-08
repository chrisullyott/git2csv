import os
import re
import csv
from urllib.parse import urlparse
from git import Git, Repo

# https://git-scm.com/docs/git-log
# https://gitpython.readthedocs.io

class LogFetcher:
    def __init__(self, repo_path, user=None):
        self.repo_path = repo_path
        self.git = Git(repo_path)
        self.name = self.get_repo_name()
        self.user = user if user else self.get_default_user()

    def get_repo_name(self):
        repo = Repo(self.repo_path)
        url = urlparse(repo.remote().url)
        basename = url.path.split('/')[-1]
        return basename.replace('.git', '')

    def get_default_user(self):
        name = self.git.config('--get', 'user.name')
        email = self.git.config('--get', 'user.email')
        return '{} <{}>'.format(name, email)

    def get_headers(self):
        return ['repo', 'sha', 'author', 'date', 'subject', 'body']

    def get_entries(self):
        entries = []
        output = self.git.log(
            '--author={}'.format(self.user),
            '--pretty=format:%H|%an <%ae>|%ai|%s|%b~~~',
            '--no-merges'
        )
        for line in output.split('~~~')[:-1]:
            entry = [self.name]
            data = line.split('|')
            for item in data:
                entry.append(item.strip())
            entries.append(entry)
        return entries

class CsvWriter:
    def __init__(self, name, data, directory=None):
        self.name = name
        self.data = data
        self.directory = directory if directory else 'output'

    def get_filepath(self):
        filename = '{}.csv'.format(self.name)
        return os.path.join(self.directory, filename)

    def write(self):
        if not os.path.exists(self.directory):
            os.mkdir(self.directory)
        with open(self.get_filepath(), 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
