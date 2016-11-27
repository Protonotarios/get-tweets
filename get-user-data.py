#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

# Φόρτωση του αρχείου ρυθμίσεων config.py 
# με τα διαπιστευτήρια για το API του Twitter 
# και τους λογαριασμούς που θέλουμε να συλλέξουμε
config = {}
execfile("config.py", config)

# Ταυτοποίηση μέσω των διαπιστευτηρίων μας στο Twitter
auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
auth.set_access_token(config['access_key'], config['access_secret'])
# Ενεργοποίηση της βιβλιοθήκης tweepy
api = tweepy.API(auth)


def get_user_data(screen_name):
    # Χρήση της μεθόδου get_user του tweepy για τη λήψη στοιχείων χρήστη
    # http://docs.tweepy.org/en/v3.5.0/api.html
    user = api.get_user(screen_name = screen_name)

    # Επιλογή των στοιχείων που μας ενδιαφέρουν από το επιστρεφόμενο json
    # Επεξήγηση των πεδίων εδώ: https://dev.twitter.com/overview/api/users
    # Τα πεδία που δύναται να περιέχουν Ελληνικά πρέπει να κωδικοποιηθούν σε UTF-8
    userdata = [user.id_str, user.screen_name, user.name.encode("utf-8"),
                user.description.encode("utf-8"), user.created_at, 
                user.location.encode("utf-8"), user.lang, user.time_zone, user.url, 
                user.profile_image_url, user.followers_count, user.friends_count, 
                user.statuses_count, user.favourites_count, user.listed_count, 
                user.verified]

    # Εγγραφή των στοιχείων ως νέα γραμμή στο csv
    writer.writerow(userdata)
	
    pass


if __name__ == '__main__':
    with open('user data.csv', 'wb') as f:
        writer = csv.writer(f)
        # Δημιουργία κεφαλίδων στηλών στο csv
        writer.writerow(['Αναγνωριστικό λογαριασμού','Όνομα λογαριασμού',
                         'Πραγματικό όνομα','Περιγραφή','Ημερομηνία δημιουργίας λογαριασμού',
                         'Τοποθεσία','Γλώσσα','Ζώνη ώρας','URL λογαριασμού',
                         'URL φωτογραφίας προφίλ','Αριθμός ακολούθων',
                         'Αριθμός ατόμων που ακολουθεί','Αριθμός tweets',
                         'Αριθμός αγαπημένων','Αριθμός λιστών στις οποίες είναι μέλος',
                         'Επαληθευμένος λογαριασμός;'])
        for account in accounts:
            print 'Λήψη στοιχείων για το λογαριασμό %s' % (account)
            get_user_data(account)
    print 'Η λήψη στοιχείων για όλους τους λογαριασμούς ολοκληρώθηκε'
