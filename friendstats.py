#!/usr/bin/env python3


# signal.signal(signal.SIGTERM, logout)
# atexit.register(logout)
import argparse

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