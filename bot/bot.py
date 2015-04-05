__author__ = 'gipmon'
import math
import time
from random import randint
import json

from instagram.client import InstagramAPI


class Bot:
    def __init__(self, config_file, tags_file):
        # Loading the configuration file, it has the access_token, user_id and others configs
        self.config = json.load(config_file)

        # Loading the tags file, it will be keep up to date while the script is running
        self.tags = json.load(tags_file)

        # Log file to output to html the debugging info about the script
        self.filename = self.config["path"] + self.config["prefix_name"] + time.strftime("%d%m%Y") + ".html"
        self.log_file = open(self.filename, "wb")

        # Initializing the Instagram API with our access token
        self.api = InstagramAPI(access_token=self.config["access_token"])

        # Likes per tag rate
        self.likes_per_tag = math.trunc(min(self.config["follows_per_hour"],
                                            self.config["likes_per_hour"]) / len(self.tags["tags"]))

    def save_tags(self):
        j = json.dumps(self.tags, indent=4)
        f = open('tags.json', 'w')
        print >> f, j
        f.close()

    def insta_write(self, to_write):
        if self.filename != self.config["path"] + self.config["prefix_name"] + time.strftime("%d%m%Y") + ".html":
            self.log_file.close()
            self.filename = self.config["path"] + self.config["prefix_name"] + time.strftime("%d%m%Y") + ".html"
            self.log_file = open(self.filename, "wb")

        if isinstance(to_write, list):
            self.log_file.write(''.join(to_write) + "<br/>")
        else:
            self.log_file.write(str(to_write) + "<br/>")
            self.log_file.flush()

    def going_sleep(self, timer):
        sleep = randint(timer, 2 * timer)
        self.insta_write("SLEEP " + str(sleep))
        time.sleep(sleep)

    def like_and_follow(self, media, likes_for_this_tag):
        try:
            var = self.api.user_relationship(user_id=media.user.id)

            if self.config["my_user_id"] != media.user.id:
                self.insta_write("--------------")
                self.insta_write(var)

                if var.outgoing_status == 'none':
                    self.insta_write("LIKE RESULT:")
                    self.insta_write(self.api.like_media(media_id=media.id))

                    self.insta_write("FOLLOW RESULT:")
                    self.insta_write(self.api.follow_user(user_id=media.user.id))

                    likes_for_this_tag -= 1

                    self.going_sleep(self.config["sleep_timer"])
                else:
                    self.going_sleep(self.config["sleep_timer"] / 2)

        except Exception, e:
            self.insta_write(str(e))
            self.insta_write("GOING SLEEP 30 min")
            time.sleep(1800)
            self.like_and_follow(media, likes_for_this_tag)

        return likes_for_this_tag

    def run(self):
        while True:
            for tag in self.tags["tags"].keys():
                tag = str(tag)

                self.insta_write("--------------------")
                self.insta_write("TAG: " + tag)
                self.insta_write("--------------------")

                self.insta_write("--------------------")
                self.insta_write("DICTIONARY STATUS:")

                for keys, values in self.tags["tags"].items():
                    self.insta_write(keys)
                    if values is not None:
                        self.insta_write(values)

                likes_for_this_tag = self.likes_per_tag

                while likes_for_this_tag > 0 and self.tags["tags"][tag] != 0:
                    if self.tags["tags"][tag] is None:
                        media_tag, self.tags["tags"][tag] = self.api.tag_recent_media(tag_name=tag,
                                                                                      count=likes_for_this_tag)
                    else:
                        media_tag, self.tags["tags"][tag] = self.api.tag_recent_media(tag_name=tag,
                                                                                      count=likes_for_this_tag,
                                                                                      max_tag_id=self.tags["tags"][tag])

                    self.insta_write("API CALL DONE")

                    if len(media_tag) == 0 or self.tags["tags"][tag] is None:
                        self.tags["tags"][tag] = 0
                        likes_for_this_tag = 0
                    else:
                        self.insta_write(self.tags["tags"][tag])
                        self.tags["tags"][tag] = self.tags["tags"][tag].split("&")[-1:][0].split("=")[1]

                    self.save_tags()

                    for m in media_tag:
                        likes_for_this_tag = self.like_and_follow(m, likes_for_this_tag)

                if reduce(lambda r, h: r and h[1] == 0, self.tags["tags"].items(), True):
                    self.insta_write("END")
                    exit(1)


if __name__ == '__main__':
    bot = Bot(open("config_bot.json", "r"), open("tags.json", "r"))
    bot.run()