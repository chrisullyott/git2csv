import argparse
import git2csv

parser = argparse.ArgumentParser(description='git2csv')
parser.add_argument('repo_path', help='The local path to a Git repository', type=str)
parser.add_argument('--author', help='The author (if not your local user)', type=str)
args = parser.parse_args()

fetcher = git2csv.LogFetcher(args.repo_path, args.author)
entries = fetcher.get_entries()

print('Found {} entries by "{}".'.format(len(entries), fetcher.user))

if len(entries) > 0:
    data = [fetcher.get_headers()] + entries
    writer = git2csv.CsvWriter(fetcher.name, data)
    writer.write()
    print('File written: {}'.format(writer.get_filepath()))
