#!/usr/bin/env python
# encoding: utf-8 # Απαραίτητο όταν υπάρχουν Ελληνικά

import tweepy #https://github.com/tweepy/tweepy
import csv

# Φόρτωση του αρχείου ρυθμίσεων config.py 
# με τα διαπιστευτήρια για το API του Twitter 
# και τους λογαριασμούς που θέλουμε να συλλέξουμε
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
    print "Λήψη της πρώτης διακοσάδας tweets"
    # Χρήση της μεθόδου user_timeline του tweepy για τη λήψη tweets
    # http://docs.tweepy.org/en/v3.5.0/api.html
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
    # Αποθήκευση των πιο πρόσφατων tweets
    alltweets.extend(new_tweets)
	
    # Αποθήκευση του αναγνωριστικού (id) του παλαιότερου από αυτά τα tweets, μείον 1
    oldest = alltweets[-1].id - 1

    print "...%s tweets έχουν ληφθεί μέχρι τώρα" % (len(alltweets))
	
    # Έναρξη βρόγχου
    # Συνεχές κατέβασμα tweets ανά διακοσάδες μέχρι να κατέβουν όλα
    while len(new_tweets) > 0:
        print "Λήψη της επόμενης διακοσάδας tweets μέχρι πριν το %s" % (oldest)
        		
        # Όλα τα αιτήματα που ακολουθούν χρησιμοποιούν την παράμετρο max_id για την αποφυγή διπλοτύπων
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest) 
        #new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id='300') # Προσωρινή εντολή - Θα διαγραφεί μετά
        
        # Αποθήκευση των πιο πρόσφατων tweets
        alltweets.extend(new_tweets)
        		
        # Ενημέρωση του αναγνωριστικού (id) του παλαιότερου από αυτά τα tweets, μείον 1
        oldest = alltweets[-1].id - 1
        		
        print "...%s tweets έχουν ληφθεί μέχρι τώρα" % (len(alltweets))
	
    # Επιλογή των στοιχείων που μας ενδιαφέρουν από το επιστρεφόμενο json
    # Επεξήγηση των πεδίων εδώ: https://dev.twitter.com/overview/api/tweets
    # Τα πεδία που δύναται να περιέχουν Ελληνικά πρέπει να κωδικοποιηθούν σε UTF-8
    # Μετατροπή των tweets σε διδιάστατο πίνακα ο οποίος μετά θα γραφτεί στο csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.retweet_count, tweet.favorite_count, tweet.text.encode("utf-8")] 
                  for tweet in alltweets]
	
    # Δημιουργία του εκάστοτε csv	
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        # Δημιουργία κεφαλίδων στηλών
        writer.writerow(["Αναγνωριστικό tweet","Ημερομηνία δημιουργίας","Αριθμός retweets","Αριθμός αγαπημένων","Κείμενο"])
        # Εγγραφή των tweets
        writer.writerows(outtweets)
  
    print "Τα tweets εγγράφηκαν στο αρχείο %s_tweets.csv" % (screen_name)
	
    pass


if __name__ == '__main__':
    for account in accounts:
        print 'Έναρξη λήψης tweets για το λογαριασμό %s' % (account)
        get_all_tweets(account)
        print 'Η λήψη tweets για το λογαριασμό %s ολοκληρώθηκε' % (account)
        print '-------------------------------'
    print 'Η λήψη tweets για όλους τους λογαριασμούς ολοκληρώθηκε'
