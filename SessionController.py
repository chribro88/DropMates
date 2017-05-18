import json
import random

import requests
import time

from User import User


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

    def __get_page(self, data):
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

        return data

    def __get_users(self, relationship):
        print("Building relationship list: %s" % relationship)

        data = self.__get_page("%s.first(20)" % relationship)
        users = []

        for node in data[relationship]['nodes']:
            users.append(User.from_node(node))

        while data[relationship]['page_info']['has_next_cursor']:
            time.sleep(1 + random.random())

            end_cursor = data[relationship]['page_info']['end_cursor']

            data = self.__get_page("%s.after(%s, 20)" % (relationship, end_cursor))

            for node in data[relationship]['nodes']:
                users.append(User.from_node(node))

        print("Found %i followers" % len(users))

        print("Finished building list: %s" % relationship)

        return users

    def get_followers(self):
        return self.__get_users("followed_by")

    def get_following(self):
        return self.__get_users("follows")

    def unfollow(self, user):
        print("Unfollowing %s" % user.full_name)

        if not self.logged_in:
            print("Not logged in, exiting")
            exit()

        response = self.session.post(SessionController.url_unfollow % user.id)

        try:
            status = json.loads(response.text)
            if status['status'] != 'ok':
                raise Exception("Failed to unfollow")
        except:
            print("Possibly unfolowing too fast")
            print("Error: %s" % response.text)
            print("Exiting to prevent ban")
            quit()

    def unfollow_all(self, user_list):
        for user in user_list:
            self.unfollow(user)

            calculated_delay = int(((SessionController.unfollow_delay + 7)
                                    - SessionController.unfollow_delay)
                                   * random.random()
                                   + SessionController.unfollow_delay)
            print('Sleeping %i seconds' % calculated_delay)
            time.sleep(calculated_delay)

    def login(self, username=None, password=None):
        print("Attempting login")

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
            'username': username,
            'password': password
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
            finder = r.text.find(username)

            if finder != -1:
                print('Logged in successfully')
                self.logged_in = True

                # populate user info
                time.sleep(3)

                user_info = self.session.get('https://www.instagram.com/%s/?__a=1' % username)
                data = json.loads(user_info.text)

                self.user_id = int(data['user']['id'])
            else:
                print('Login failed, possible cred issue')
                quit()
        else:
            print('Login failed, non-200')
            print('Lode %i found' % login.status_code)
            quit()

    def logout(self):
        if self.logged_in:
            time.sleep(1)

            try:
                print('Logging out...')

                logout_post = {'csrfmiddlewaretoken': self.csrftoken}
                self.session.post(SessionController.url_logout, data=logout_post)
            except:
                print('Failed to logout')