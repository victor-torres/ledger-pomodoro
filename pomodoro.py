#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import json
import os
import requests
import sys
import urllib

token = os.environ['SLACK_API_TOKEN']

args = sys.argv[1:]
last_arg = args and args[-1] or ''
emoji = ''
if last_arg.startswith(':') and last_arg.endswith(':'):
    emoji = last_arg
    args = args[:-1]

text = args and ' '.join(args) or ''

profile =  {
    'first_name': os.environ['SLACK_FIRST_NAME'],
    'last_name': os.environ['SLACK_LAST_NAME'],
    'status_text': text,
    'status_emoji': emoji,
}

profile = json.dumps(profile)
profile = urllib.quote(profile)
url = "https://slack.com/api/users.profile.set"
payload = "token={token}&profile={profile}".format(token=token, profile=profile)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
}

def get_filename():
    date = datetime.datetime.today().strftime('%Y-%m')
    return '{0}.ledger'.format(date)

def get_datetime():
    date = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    return date

with open(get_filename(), 'r') as f:
    lines = f.readlines()

lines = filter(lambda l: 'Pomodoro' in l, lines)
last_line = lines and lines[-1]

with open(get_filename(), 'a') as f:
    if last_line and last_line.startswith('i'):
        close_text = last_line.split('\t')[1].split('\n')[0]
        f.write('o {0} Pomodoro\t{1}\n'.format(get_datetime(), close_text))

    if text:
        f.write('i {0} Pomodoro\t{1}\n'.format(get_datetime(), text))

response = requests.request("POST", url, data=payload, headers=headers)
response = json.loads(response.text)

if response.get('ok'):
    print 'Published on Slack'
else:
    print 'Failed to publish on Slack'

