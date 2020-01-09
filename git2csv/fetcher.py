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
        self.headers = ['repo', 'sha', 'author', 'date', 'subject', 'body']

    def get_repo_name(self):
        repo = Repo(self.repo_path)
        url = urlparse(repo.remote().url)
        basename = url.path.split('/')[-1]
        return basename.replace('.git', '')

    def get_default_user(self):
        name = self.git.config('--get', 'user.name')
        email = self.git.config('--get', 'user.email')
        return '{} <{}>'.format(name, email)

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
