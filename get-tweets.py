#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

# ΑΡΧΙΚΕΣ ΜΕΤΑΒΛΗΤΕΣ

# Εδώ βάζουμε τους λογαριασμούς Twitter που θέλουμε να κατεβάσουμε
# Μπορούμε να βάλουμε όσους θέλουμε
# Ενδεικτικά έχω βάλει 3 λογαριασμούς Ελλήνων πολιτικών
# Εσείς βάλτε τους δικούς σας
accounts = ['AdonisGeorgiadi','PanosKammenos','rachelmakri']

# ΜΗΝ ΑΛΛΑΞΕΤΕ ΚΑΤΙ ΑΠΟ ΔΩ ΚΑΙ ΚΑΤΩ

# Φορτώνουμε τα διαπιστευτήρια για το API του Twitter που βρίσκονται στο αρχείο config.py
config = {}
execfile("config.py", config)


def get_all_tweets(screen_name):
	# Το Twitter επιτρέπει μέσω του API τη λήψη μόνο των τελευταίων 3240 tweets ενός χρήστη
	
	# Ταυτοποίηση μέσω των διαπιστευτηρίων μας στο Twitter
	auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
	auth.set_access_token(config['access_key'], config['access_secret'])
	# Ενεργοποίηση της βιβλιοθήκης tweepy
	api = tweepy.API(auth)
	
	# Δημιουργία μιας κενής λίστας η οποία θα κρατάει όλα τα tweets
	alltweets = []	
	
	# Το αρχικό αίτημα για τα 200 πιο πρόσφατα tweets (τόσα επιτρέπονται σε ένα αίτημα)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	# Αποθήκευση των πιο πρόσφατων tweets
	alltweets.extend(new_tweets)
	
	# Αποθήκευση του αναγνωριστικού (id) του παλαιότερου από αυτά τα tweets, μείον 1
	oldest = alltweets[-1].id - 1
	
	# Έναρξη βρόγχου
	# Συνεχές κατέβασμα tweets ανά διακοσάδες μέχρι να κατέβουν όλα
	while len(new_tweets) > 0:
		print "λήψη των tweets πριν το %s" % (oldest)
		
		# Όλα τα αιτήματα που ακολουθούν χρησιμοποιούν την παράμετρο max_id για την αποφυγή διπλοτύπων
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest) 
		#new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id='300') # Προσωρινή εντολή - Θα διαγραφεί μετά

		# Αποθήκευση των πιο πρόσφατων tweets
		alltweets.extend(new_tweets)
		
		# Ενημέρωση του αναγνωριστικού (id) του παλαιότερου από αυτά τα tweets, μείον 1
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets κατέβηκαν μέχρι τώρα" % (len(alltweets))
	
	# Μετατροπή των tweets σε διδιάστατο πίνακα ο οποίος μετά θα γραφτεί στο csv
	outtweets = [[tweet.id_str, tweet.created_at, tweet.retweet_count, tweet.favorite_count, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	# Εγγραφή στο csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","retweet_count","favorite_count","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	for account in accounts:
		get_all_tweets(account)
