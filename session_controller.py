import json
import random

import requests
import time
import logging

from user import User

logger = logging.getLogger('stats')


class SessionController:
    url = 'https://www.instagram.com/'
    url_login = url + 'accounts/login/ajax/'
    url_logout = url + 'accounts/logout/'
    url_follow = url + 'web/friendships/%s/follow/'
    url_unfollow = url + 'web/friendships/%s/unfollow/'
    url_query = url + 'query/'

    unfollow_delay = 0

    def __init__(self):
        self.logged_in = False
        self.user_id = None
        self.session = requests.Session()
        self.csrftoken = ''
        self.username = None
        self.password = None

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def __get_page(self, data):
        logger.info("Getting page with data")
        logger.debug("Page data: %s" % data)

        post = {
            'q': 'ig_user(%i) { \
                   %s { ' % (self.user_id, data) +
                 'count, \
                 page_info { \
                   end_cursor, \
                   has_next_page \
                 }, \
                 nodes { \
                   id, \
                   is_verified, \
                   followed_by_viewer, \
                   requested_by_viewer, \
                   full_name, \
                   profile_pic_url, \
                   username \
                 } \
               } \
             }',
            'ref': 'relationships::follow_list',
            'query_id': '17845270936146575'
        }

        response = self.session.post(SessionController.url_query, data=post)
        data = json.loads(response.text)

        logger.info("Finish getting users from page")
        return data

    def __get_users(self, relationship):
        logger.info("Building relationship list: %s" % relationship)

        if not self.logged_in:
            self.login()

        data = self.__get_page("%s.first(20)" % relationship)
        users = []

        for node in data[relationship]['nodes']:
            users.append(User.from_node(node))

        while data[relationship]['page_info']['has_next_page']:
            time.sleep(1 + random.random())

            end_cursor = data[relationship]['page_info']['end_cursor']

            data = self.__get_page("%s.after(%s, 20)" % (relationship, end_cursor))

            for node in data[relationship]['nodes']:
                users.append(User.from_node(node))

        logger.info("Found %i followers" % len(users))
        logger.info("Finished building list: %s" % relationship)

        return users

    def get_followers(self):
        return self.__get_users("followed_by")

    def get_following(self):
        return self.__get_users("follows")

    def unfollow(self, user):
        print("Unfollowing @%s" % user.username)

        if not self.logged_in:
            self.login()

        try:
            response = self.session.post(SessionController.url_unfollow % user.id)
            status = json.loads(response.text)
            if status['status'] != 'ok':
                raise Exception("Failed to unfollow")
        except:
            logger.warning("Possibly unfolowing too fast")
            logger.warning("Exiting to prevent ban")
            quit()

    def unfollow_all(self, user_list):
        logger.info("Unfollowing %i users" % len(user_list))
        for user in user_list:
            self.unfollow(user)

            calculated_delay = int(((SessionController.unfollow_delay + 7)
                                    - SessionController.unfollow_delay)
                                   * random.random()
                                   + SessionController.unfollow_delay)
            logger.debug('Sleeping %i seconds' % calculated_delay)
            time.sleep(calculated_delay)

        logger.info("Finished unfollowing user list")

    def login(self):
        logger.info("Attempting login")

        self.session.cookies.update({
            'sessionid': '',
            'mid': '',
            'ig_pr': '1',
            'ig_vw': '1920',
            'csrftoken': '',
            's_network': '',
            'ds_user_id': ''
        })

        login_details = {
            'username': self.username,
            'password': self.password
        }

        self.session.headers.update({
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36'),
            'X-Instagram-AJAX': '1',
            'X-Requested-With': 'XMLHttpRequest'
        })

        # get the csrf token from a typical request
        r = self.session.get(SessionController.url)
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})

        time.sleep(5 * random.random())

        # do login
        login = self.session.post(SessionController.url_login, data=login_details, allow_redirects=True)
        self.session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']

        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.session.get('https://www.instagram.com/')
            finder = r.text.find(self.username)

            if finder != -1:
                logger.info('Logged in successfully')
                self.logged_in = True

                # populate user info
                time.sleep(3)

                user_info = self.session.get('https://www.instagram.com/%s/?__a=1' % self.username)
                data = json.loads(user_info.text)

                self.user_id = int(data['user']['id'])
            else:
                logger.warning('Login failed, possible cred issue')
                quit()
        else:
            logger.warning('Login failed, non-200')
            logger.warning('Lode %i found' % login.status_code)
            quit()

    def logout(self):
        if self.logged_in:
            time.sleep(1)

            try:
                logger.info('Logging out...')

                logout_post = {'csrfmiddlewaretoken': self.csrftoken}
                self.session.post(SessionController.url_logout, data=logout_post)
            except:
                logger.warning('Failed to logout')
