#!/usr/bin/env python3


# signal.signal(signal.SIGTERM, logout)
# atexit.register(logout)
import argparse

from FileRepository import read_json
from SessionController import SessionController


class Application:
    filestore = "cache.json"

    def __init__(self, username, password, rebuild):
        self.session = SessionController()
        self.followers = []
        self.following = []

        # self.session.login(username, password)
        if not rebuild:
            self.read_cache()

        if not self.followers and not self.following:
            self.rebuild_cache()

    def read_cache(self):
        cache = read_json(Application.filestore)

        if cache:
            try:
                self.followers = cache['followers']
                self.following = cache['following']
                return True
            except:
                print("Failed to read cache")

        return False

    def rebuild_cache(self):
        pass

    def close(self):
        self.session.logout()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze and process instagram followers')

    parser.add_argument("-u", "--username", help='Instagram username')
    parser.add_argument("-p", "--password", help='Instagram password')
    parser.add_argument("-c", "--config", help='Application config file')
    parser.add_argument("-r", "--rebuild", action="store_true", help='Rebuild the user cache from the web')
    parser.add_argument("-v", "--verified", action="store_true", help='Filter by hiding verified users')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--followers", action="store_true", help="Show your followers")
    group.add_argument("-o", "--following", action="store_true", help="Show the user that you follow")
    group.add_argument("-s", "--shame", action="store_true", help="Show those users that don't follow you back")

    args = parser.parse_args()

    app = None
    username = args.username
    password = args.password
    if not username and not password and args.config:
        config = read_json(args.config)
        username = config['username']
        password = config['password']

    if not username and not password:
        print("No credentials found")
        exit()

    app = Application(username, password, args.rebuild)

    app.close()