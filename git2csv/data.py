import os
import re
import csv
from urllib.parse import urlparse
from git import Git, Repo

# https://git-scm.com/docs/git-log
# https://gitpython.readthedocs.io

class CsvBuilder:
    def __init__(self, repo_path):
        self.git = Git(repo_path)
        self.repo = Repo(repo_path)

    def get_user(self):
        name = self.git.config('--get', 'user.name')
        email = self.git.config('--get', 'user.email')
        return '{} <{}>'.format(name, email)

    def get_name(self):
        url = urlparse(self.repo.remote().url)
        basename = url.path.split('/')[-1]
        return basename.replace('.git', '')

    def get_log_rows(self):
        rows = [['sha', 'author', 'date', 'subject', 'body']]
        output = self.git.log(
            '--author={}'.format(self.get_user()),
            '--pretty=format:%H|%an <%ae>|%ad|%s|%b~~~',
            '--no-merges'
        )
        for line in output.split('~~~')[:-1]:
            row = []
            data = line.split('|')
            for i in data[:-1]:
                row.append(i.strip())
            row.append(re.sub(r'\s+', ' ', data[-1]))
            rows.append(row)
        return rows

    def write(self, directory=None):
        filename = '{}.csv'.format(self.get_name())
        if not directory:
            directory = 'output'
        if not os.path.exists(directory):
            os.mkdir(directory)
        filename = os.path.join(directory, filename)
        with open(filename, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.get_log_rows())
