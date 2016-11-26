#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import json

#pass in the usernames of the accounts you want to download
accounts = ['AdonisGeorgiadi','PanosKammenos','rachelmakri']

# load our API credentials from config.py file
config = {}
execfile("config.py", config)

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
auth.set_access_token(config['access_key'], config['access_secret'])
api = tweepy.API(auth)


def get_user_data(screen_name):
	user = api.get_user(screen_name = screen_name)

	userdata = [user.id_str, user.screen_name, user.name.encode("utf-8"), user.description.encode("utf-8"), user.created_at, user.location.encode("utf-8"), user.lang, user.time_zone, user.url, user.profile_image_url, user.followers_count, user.friends_count, user.statuses_count, user.favourites_count, user.listed_count, user.verified]

	writer.writerow(userdata)
	
	pass


if __name__ == '__main__':
	with open('user data.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['Αναγνωριστικό λογαριασμού','Όνομα λογαριασμού','Πραγματικό όνομα','Περιγραφή','Ημερομηνία δημιουργίας λογαριασμού','Τοποθεσία','Γλώσσα','Ζώνη ώρας','URL λογαριασμού','URL φωτογραφίας προφίλ','Αριθμός ακολούθων','Αριθμός ατόμων που ακολουθεί','Αριθμός tweets','Αριθμός αγαπημένων','Αριθμός λιστών στις οποίες είναι μέλος','Επαληθευμένος λογαριασμός;'])
		for account in accounts:
			get_user_data(account)
