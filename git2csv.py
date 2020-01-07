import argparse
import git2csv

parser = argparse.ArgumentParser(description='git2csv')
parser.add_argument('repo_path', help='The local path to a Git repository', type=str)
args = parser.parse_args()

g2c = git2csv.CsvBuilder(args.repo_path)
g2c.write()
