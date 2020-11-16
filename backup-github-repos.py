#! /usr/bin/env python3

import argparse
import datetime
import json
import os
import shutil
import subprocess
import urllib.request


def get_now():
    return datetime.datetime.now(datetime.timezone.utc)


def format_datetime(dt):
    return dt.strftime('%Y%m%dT%H%M%SZ')


def get_directory_name(username, now):
    return f'github-backup-{username}-{format_datetime(now)}'


def get_archive_name(username, now):
    return f'{get_directory_name(username, now)}.tar.gz'


def parse_args():
    p = argparse.ArgumentParser(description='''Back up the repositories
            of a GitHub user.''',
            epilog='''This program will create a file named similar to ''' +
            get_archive_name('UserName', get_now()) +
            ''' in your current directory.''')
    p.add_argument('username', help='''The GitHub user
            whose repositories to back up.''')
    return p.parse_args()


def get_clone_urls(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as f:
        return tuple(repo['clone_url'] for repo in json.load(f))


def clone_repos(username, now):
    dir_name = get_directory_name(username, now)
    os.mkdir(dir_name)
    for clone_url in get_clone_urls(username):
        subprocess.run(['git', 'clone', clone_url], check=True, cwd=dir_name)


def archive(username, now):
    subprocess.run(['tar', 'czf', get_archive_name(username, now),
        get_directory_name(username, now)], check=True)


def main():
    args = parse_args()
    now = get_now()
    clone_repos(args.username, now)
    archive(args.username, now)
    shutil.rmtree(get_directory_name(args.username, now))


if __name__ == '__main__':
    main()
