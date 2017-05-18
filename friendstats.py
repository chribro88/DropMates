#!/usr/bin/env python3

import requests
import random
import time
import json
import atexit
import signal
import sys
import datetime
import os.path

from SessionController import SessionController

if not os.path.isfile('config.json'):
    print('please create a config.json file (config_sammple.json in root)')
    quit()

with open('config.json', 'r') as fp:
    try:
        config = json.load(fp)
    except:
        print('invalid config.json file (probably parsing issue)')
        quit()


session_ctrl = SessionController()


def start_sync():
    login()

    user_followers = session_ctrl.get_followers()

    user_following = session_ctrl.get_following()

    diff = set(user_following) - set(user_followers)

    print('found %i people who you follow but don\'t follow you back' % (len(diff)))

    with open('state.json', 'w') as user_state:
        print('writing data to state.json')

        json.dump({
            'version': '0.0.1',
            'state_date': datetime.datetime.now().isoformat(),
            'followers': {
                'data': user_followers
            },
            'following': {
                'data': user_following
            }
        }, user_state, indent=4, sort_keys=True)
        user_state.close()


def load_sync():
    if not os.path.isfile('state.json'):
        print('no state.json to load, please run a sync with option 1 or 2')
        quit()

    fp = open('state.json', 'r')
    user_state = json.load(fp)
    fp.close()

    unfollow_list = set(user_state['following']['data']) - set(user_state['followers']['data'])

    if len(unfollow_list) <= 0:
        print('nobody to unfollow')
        quit()

    session_ctrl.unfollow_all(unfollow_list)






signal.signal(signal.SIGTERM, logout)
atexit.register(logout)

menu()
