import logging

from file_repository import read_pickle, write_pickle

logger = logging.getLogger('stats')


class UserService:
    filestore = "cache.pickle"

    def __init__(self):
        self.followers = []
        self.following = []

    def read_cache(self):
        logger.info("Reading cache")
        cache = read_pickle(UserService.filestore)

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

    def rebuild_cache(self, session):
        logger.info("Rebuilding cache")
        self.followers = session.get_followers()
        self.following = session.get_following()

        logger.debug("Writing cache to file")
        write_pickle({
            "followers": self.followers,
            "following": self.following
        }, UserService.filestore)
        logger.info("Finish rebuilding cache")

    def __find_users(self, u_list, verified):
        if verified:
            u_list = [u for u in u_list if not u.is_verified]

        return u_list

    def find_followers(self, verified):
        return self.__find_users(self.followers, verified)

    def find_following(self, verified):
        return self.__find_users(self.following, verified)

    def find_shame(self, verified):
        return self.__find_users(set(self.following) - set(self.followers), verified)
