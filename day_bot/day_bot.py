__author__ = 'gipmon'
from instagram.client import InstagramAPI
import math
import time
import datetime
from random import randint
import json


#Loading the configuration file, it has the access_token, user_id and others configs
config_file = open("config_bot.json", "r")
config = json.load(config_file)

#Loading the tags file, it will be keep up to date while the script is running
tags_file = open("tags.json", "r")
tags = json.load(tags_file)

#Log file to output to html the debugging info about the script
filename = config["path"]+config["prefix_name"]+time.strftime("%d%m%Y")+".html"
log_file = open(filename, "wb")

#Initializing the Instagram API with our access token
api = InstagramAPI(access_token=config["access_token"])

#Likes per tag rate
likes_per_tag = math.trunc(min(config["follows_per_hour"], config["likes_per_hour"])/len(tags["tags"]))

#1422403200

def insta_write(to_write):
    global filename, log_file
    if filename != config["path"]+config["prefix_name"]+time.strftime("%d%m%Y")+".html":
        log_file.close()
        filename = config["path"]+config["prefix_name"]+time.strftime("%d%m%Y")+".html"
        log_file = open(filename, "wb")

    if isinstance(to_write, list):
        log_file.write(''.join(to_write)+"<br/>")
    else:
        log_file.write(str(to_write)+"<br/>")
    log_file.flush()


def going_sleep(timer):
    #sleep for x seconds
    sleep = randint(timer, 2*timer)
    insta_write("SLEEP "+str(sleep))
    time.sleep(sleep)


def like_and_follow(media):
    global api, likes_for_this_tag
    try:
        var = api.user_relationship(user_id=media.user.id)

        if config["my_user_id"] != media.user.id:
            insta_write("--------------")
            insta_write(var)

            if var.outgoing_status == 'none':
                insta_write("LIKE RESULT:")
                insta_write(api.like_media(media_id=media.id))

                insta_write("FOLLOW RESULT:")
                insta_write(api.follow_user(user_id=media.user.id))

                likes_for_this_tag -= 1

                going_sleep(config["sleep_timer"])
            else:
                going_sleep(config["sleep_timer"]/2)

    except Exception, e:
        insta_write(str(e))
        insta_write("GOING SLEEP 30 min")
        time.sleep(1800)
        like_and_follow(media)


#carregar a ultima data verificada
f = open('daybot_time', 'r')
ts = float(f.readline())
f.close()
last_date = datetime.datetime.fromtimestamp(ts)

#guardar a data num ficheiro
f = open('daybot_time', 'w')
f.write(str(time.time()))
f.close()
#1422403200

while True:
    for tag in tags["tags"].keys():
        insta_write("--------------------")
        insta_write("TAG: "+tag)
        insta_write("--------------------")

        insta_write("--------------------")
        insta_write("DICTIONARY STATUS:")
        for keys, values in tags["tags"].items():
            insta_write(keys)
            if values is not None:
                insta_write(values)

        likes_for_this_tag = likes_per_tag

        while likes_for_this_tag > 0 and tags["tags"][tag] != 0:
                if tags["tags"][tag] is None:
                    media_tag, tags["tags"][tag] = api.tag_recent_media(tag_name=tag, count=likes_for_this_tag)
                else:
                    media_tag, tags["tags"][tag] = api.tag_recent_media(tag_name=tag, count=likes_for_this_tag,
                                                                max_tag_id=tags["tags"][tag])

                insta_write("API CALL DONE")

                #se todos tiverem data superior a carregada morre
                date_all_higher = False

                for media in media_tag:
                    date_all_higher |= (media.created_time > last_date)
                    #print media.created_time > last_date

                if not date_all_higher:
                    insta_write("DONE!")
                    exit(1)

                if len(media_tag) == 0 or tags["tags"][tag] is None:
                    tags["tags"][tag] = 0
                    if reduce(lambda r, h: r and h == 0, tags["tags"].items(), True):
                        insta_write("END")
                        exit(1)
                    else:
                        likes_for_this_tag = 0
                else:
                    insta_write(tags["tags"][tag])
                    tags["tags"][tag] = tags["tags"][tag].split("&")[-1:][0].split("=")[1]

                for m in media_tag:
                    #verify if date is higher
                    like_and_follow(m)