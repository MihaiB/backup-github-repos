#! /usr/bin/env python3

import argparse
import datetime

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
            epilog='''This program will produce ''' +
            get_archive_name('UserName', get_now()) +
            ''' in the current directory.''')
    p.add_argument('username', help='''The GitHub user
            whose repositories to back up.''')
    return p.parse_args()

def main():
    args = parse_args()
    print(args)

if __name__ == '__main__':
    main()
