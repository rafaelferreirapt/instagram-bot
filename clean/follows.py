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
            self.follows()

    def follows(self, next_page=None):
        print "next_page: ", next_page

        try:
            if next_page is None:
                follows, next_ = self.api.user_follows(user_id=self.config['my_user_id'])
            else:
                follows, next_ = self.api.user_follows(user_id=self.config['my_user_id'], with_next_url=next_page)

            for follow in follows:
                var = self.api.user_relationship(user_id=follow.id)
                print var.incoming_status, follow.id

                if var.incoming_status == 'none':
                    self.api.unfollow_user(user_id=follow.id)

                var = self.api.user_relationship(user_id=follow.id)
                print var.outgoing_status, follow.id

            return self.follows(next_)
        except Exception, e:
            print e
            time.sleep(1800)
            return self.follows(next_page)


if __name__ == '__main__':
    clean = CleanFollows(open("config_clean.json", "r"))
    clean.run()