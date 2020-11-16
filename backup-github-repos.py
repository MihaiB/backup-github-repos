#! /usr/bin/env python3

import argparse
import datetime
import json
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
            epilog='''This program will create the file ''' +
            get_archive_name('UserName', get_now()) +
            ''' in the current directory.''')
    p.add_argument('username', help='''The GitHub user
            whose repositories to back up.''')
    return p.parse_args()


def get_clone_urls(username):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Accept': 'application/vnd.github.v3+json'}
    request = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(request) as f:
        data = json.load(f)

    return tuple(repo['clone_url'] for repo in data)


def main():
    args = parse_args()
    clone_urls = get_clone_urls(args.username)
    for url in clone_urls:
        print(url)


if __name__ == '__main__':
    main()
