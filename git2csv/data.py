import os
import re
import csv
from urllib.parse import urlparse
from git import Git, Repo

# https://git-scm.com/docs/git-log
# https://gitpython.readthedocs.io

class LogFetcher:
    def __init__(self, repo_path, user=None):
        self.git = Git(repo_path)
        self.repo = Repo(repo_path)
        self.user = user

    def get_user(self):
        if not self.user:
            name = self.git.config('--get', 'user.name')
            email = self.git.config('--get', 'user.email')
            return '{} <{}>'.format(name, email)
        return self.user

    def get_name(self):
        url = urlparse(self.repo.remote().url)
        basename = url.path.split('/')[-1]
        return basename.replace('.git', '')

    def get_headers(self):
        return ['sha', 'author', 'date', 'subject', 'body']

    def get_entries(self):
        entries = []
        output = self.git.log(
            '--author={}'.format(self.get_user()),
            '--pretty=format:%H|%an <%ae>|%ad|%s|%b~~~',
            '--no-merges'
        )
        for line in output.split('~~~')[:-1]:
            entry = []
            data = line.split('|')
            for i in data[:-1]:
                entry.append(i.strip())
            entry.append(re.sub(r'\s+', ' ', data[-1]))
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
