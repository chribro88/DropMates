import logging
import Colors

logger = logging.getLogger('stats')


class User:
    def __init__(self, user_id, username, full_name, is_verified, followed_by_viewer,
                 requested_by_viewer, profile_pic_url):
        self.id = user_id
        self.username = username
        self.full_name = full_name
        self.is_verified = is_verified
        self.followed_by_viewer = followed_by_viewer
        self.requested_by_viewer = requested_by_viewer
        self.profile_pic_url = profile_pic_url

    def __str__(self):
        out = None
        if self.is_verified:
            out = Colors.OKBLUE + "[x]" + Colors.ENDC
        else:
            out = "[ ]"

        out += " %s" % self.username

        return out

    @classmethod
    def from_node(cls, node):
        logger.debug("Creating User from node")
        logger.debug(node)
        return cls(node['id'], node['username'], node['full_name'], node['is_verified'],
                   node['followed_by_viewer'], node['requested_by_viewer'], node['profile_pic_url'])

