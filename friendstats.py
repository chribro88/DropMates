#!/usr/bin/env python3


# signal.signal(signal.SIGTERM, logout)
# atexit.register(logout)
import argparse

import logging

from FileRepository import read_json, write_json, write_pickle, read_pickle
from SessionController import SessionController
from Logger import create_logger

logger = create_logger("stats")


class Application:
    filestore = "cache.pickle"

    def __init__(self, username, password, rebuild):
        self.session = SessionController()
        self.followers = []
        self.following = []

        self.session.set_credentials(username, password)
        if not rebuild:
            self.read_cache()

        if not self.followers and not self.following:
            self.rebuild_cache()

    def read_cache(self):
        logger.info("Reading cache")
        cache = read_pickle(Application.filestore)

        if cache:
            try:
                self.followers = cache['followers']
                self.following = cache['following']

                logger.info("Cache read successfully")
                logger.info("Followers: %i" % len(self.followers))
                logger.info("Following: %i" % len(self.following))

                return True
            except:
                logger.warning("Failed to read cache")

        return False

    def rebuild_cache(self):
        self.followers = self.session.get_followers()
        self.following = self.session.get_following()

        write_pickle({
            "followers": self.followers,
            "following": self.following
        }, Application.filestore)

    def close(self):
        self.session.logout()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Analyze and process instagram followers')

    parser.add_argument("-u", "--username", help='Instagram username')
    parser.add_argument("-p", "--password", help='Instagram password')
    parser.add_argument("-c", "--config", help='Application config file')
    parser.add_argument("-r", "--rebuild", action="store_true", help='Rebuild the user cache from the web')
    parser.add_argument("-x", "--verified", action="store_true", help='Filter by hiding verified users')
    parser.add_argument("-v", "--verbose", action="store_true", help='Verbose logging')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--followers", action="store_true", help="Show your followers")
    group.add_argument("-o", "--following", action="store_true", help="Show the user that you follow")
    group.add_argument("-s", "--shame", action="store_true", help="Show those users that don't follow you back")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    app = None
    un = args.username
    pw = args.password
    if not un and not pw and args.config:
        logger.debug("Reading username and password from config file")
        config = read_json(args.config)
        un = config['username']
        pw = config['password']

    if not un and not pw:
        logger.warn("No credentials found")
        exit()

    app = Application(un, pw, args.rebuild)

    app.close()