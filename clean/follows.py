__author__ = 'gipmon'
import time
import json

from instagram.client import InstagramAPI


class CleanFollows:
    def __init__(self, config_file):
        # Loading the configuration file, it has the access_token, user_id and others configs
        self.config = json.load(config_file)

        # Initializing the Instagram API with our access token
        self.api = InstagramAPI(access_token=self.config["access_token"])

    def run(self):
        while True:
            try:
                self.follows()
            except Exception, e:
                time.sleep(1800)

    def follows(self, next_page=None):
        if next_page is None:
            follows = self.api.user_follows(user_id=self.config['my_user_id'])
        else:
            follows = self.api.user_follows(user_id=self.config['my_user_id'], max_tag_id=next_page)

        time.sleep(1)
        for follow in follows[0]:
            var = self.api.user_relationship(user_id=follow.id)
            print var.incoming_status

            if var.incoming_status == 'none':
                time.sleep(1)
                self.api.unfollow_user(user_id=follow.id)

            var = self.api.user_relationship(user_id=follow.id)
            print var.outgoing_status

            time.sleep(1)

        return self.follows(follows[1].split("&")[-1:][0].split("=")[1])


if __name__ == '__main__':
    clean = CleanFollows(open("config_clean.json", "r"))
    clean.run()