**The ability to POST and DELETE likes, follows and comments is restricted to applications that offer business services and not consumer facing apps.**
[https://help.instagram.com/contact/185819881608116](https://help.instagram.com/contact/185819881608116)

Instagram Python Bot
===================

This Instagram Python script let you launch one bot to like and follow people that post media with specific "tags".
You have, for now, 3 different bots:

 - The "all-time bot", **/bot**, that runs continuously  from the moment that started to the moment end of the media list for each tag.
 - The "day bot", **/day_bot**, that makes the same work of the previous one but with the difference that only likes media from the past hours.
 - The "clean bot", **/clean**, this bot cleans the following list. Now, only can clean the ones that doesn't follow you.

----------

## Configuration ##

 - **/bot** .. *config_bot.json*:
	 - "path" the folder that you want to save the log from this bot
	 - "access_token" generate from: *get_access_token.py*
	 - "my_user_id" your user id, get from the response of: *get_access_token.py*
	 - "prefix_name" the files prefix
	 - "follows_per_hour" the max rating follow
	 - "likes_per_hour" the max likes per hour
	 - "sleep_timer" sleep timer between each api_request
 - **/day_bot** .. *config_bot.json*
	 - "path" the folder that you want to save the log from this bot
	 - "access_token" generate from: *get_access_token.py*
	 - "my_user_id" your user id, get from the response of: *get_access_token.py*
	 - "prefix_name" the files prefix
	 - "follows_per_hour" the max rating follow
	 - "likes_per_hour" the max likes per hour
	 - "sleep_timer" sleep timer between each api_request
 - **/clean** .. *config_clean.json*
	 - "access_token" generate from: *get_access_token.py*
	 - "my_user_id" your user id, get from the response of: *get_access_token.py*

----------

## Installation ##
*Use a Raspberry PI!*

 1. Clone this repository to a folder
 2. Configure the bot's
 3. Launch the **screen**:
 
	```
	// Bash:
	
	screen -S SCREEN_NAME -d -m -L python ~/PATH_TO_BOT/bot.py
	```
	
 4. Crontab for **day_bot.py**:
 
	```
	// Bash:
	
	$ crontab -e
	
	00 5 * * * cd ~/PATH_TO_DAY_BOT/ && python day_bot.py
	```


----------


**More information: [http://www.rafaelferreira.pt/instagram-python-bot/](http://www.rafaelferreira.pt/instagram-python-bot/)**
