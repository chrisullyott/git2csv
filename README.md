# git2csv

Easily save a record of your commits as a CSV file.

Uses [GitPython](https://gitpython.readthedocs.io) with Python3 to build a history of your work in CSV format.

### Setup

```
$ pip3 install -r requirements.txt
```

### Run

```
$ python3 git2csv.py <LOCAL_REPOSITORY_PATH>
```

Files will be saved in a created `output` directory. Included in the data are the hash, author details, date, subject and body of the commit, like below. The body text is sanitized slightly in order to keep the CSV formatting intact.

```
sha,author,date,subject,body
2fd46a531d8ce6db70e38e259b5c5debc29900a9,First Last <me@example.com>,Mon Dec 23 21:30:30 2019 -0800,Update file again,This was tricky.,
117a7df2f87ed999813de921ce9dd2e58f868fcf,First Last <me@example.com>,Mon Dec 23 21:09:56 2019 -0800,Update file,This was easy.,
b5babe9da2c890faff26a7452c08fa2a14d270dc,First Last <me@example.com>,Sun Dec 22 14:16:03 2019 -0800,First commit,
```
