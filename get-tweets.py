#!/usr/bin/env python
# encoding: utf-8 

import tweepy #https://github.com/tweepy/tweepy
import csv
from datetime import datetime, timedelta
from unidecode import unidecode #pip install unidecode

# Φόρτωση του αρχείου ρυθμίσεων config.py 
# με τα διαπιστευτήρια για το API του Twitter 
# και τους λογαριασμούς που θέλουμε να συλλέξουμε
config = {}
execfile('config.py', config)

# Φόρτωση του λεξικού, ως greeklish
lexico = {}
for line in open(config['lexicon']):
    word, score = line.split()
    greeklish_word = unidecode(word.decode('utf-8'))
    lexico[greeklish_word] = int(score)
    

combined_out_tweets = []
# Ορισμός μέγιστης και ελάχιστης ημερομηνία στη σημερινή
min_date = max_date = datetime.now().date()

# Απλώς ένα διαχωριστικό για τις εκτυπώσεις
hr = '-'*40+'\n'

def get_all_tweets(screen_name):
    global min_date, hr
    
    # Το Twitter επιτρέπει μέσω του API τη λήψη μόνο των τελευταίων 3240 tweets ενός χρήστη
    
    # Ταυτοποίηση μέσω των διαπιστευτηρίων μας στο Twitter
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_key'], config['access_secret'])
    # Ενεργοποίηση της βιβλιοθήκης tweepy
    api = tweepy.API(auth)
	
    # Δημιουργία μιας κενής λίστας η οποία θα κρατάει όλα τα tweets
    alltweets = []	
	
    # Το αρχικό αίτημα για τα 200 πιο πρόσφατα tweets (τόσα επιτρέπονται σε ένα αίτημα)
    print 'Λήψη της πρώτης διακοσάδας tweets'
    # Χρήση της μεθόδου user_timeline του tweepy για τη λήψη tweets
    # http://docs.tweepy.org/en/v3.5.0/api.html
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
    # Αποθήκευση των πιο πρόσφατων tweets
    alltweets.extend(new_tweets)
	
    # Αποθήκευση του αναγνωριστικού (id) του παλαιότερου από αυτά τα tweets, μείον 1
    oldest = alltweets[-1].id - 1

    print '...%s tweets έχουν ληφθεί μέχρι τώρα' % (len(alltweets))
	
    # Έναρξη βρόγχου
    # Συνεχές κατέβασμα tweets ανά διακοσάδες μέχρι να κατέβουν όλα
    while len(new_tweets) > 0:
        print 'Λήψη της επόμενης διακοσάδας tweets μέχρι πριν το %s' % (oldest)
        		
        # Όλα τα αιτήματα που ακολουθούν χρησιμοποιούν την παράμετρο max_id για την αποφυγή διπλοτύπων
        #new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest) 
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id='300') # Προσωρινή εντολή - Θα διαγραφεί μετά
        
        # Αποθήκευση των πιο πρόσφατων tweets
        alltweets.extend(new_tweets)
        		
        # Ενημέρωση του αναγνωριστικού (id) του παλαιότερου από αυτά τα tweets, μείον 1
        oldest = alltweets[-1].id - 1
        		
        print '...%s tweets έχουν ληφθεί μέχρι τώρα' % (len(alltweets))
	
    # Επιλογή των στοιχείων που μας ενδιαφέρουν από το επιστρεφόμενο json
    # Επεξήγηση των πεδίων: https://dev.twitter.com/overview/api/tweets
    # Τα πεδία που δύναται να περιέχουν Ελληνικά πρέπει να κωδικοποιηθούν σε UTF-8
    # Μετατροπή των tweets σε διδιάστατο πίνακα ο οποίος μετά θα γραφτεί στο csv

    print hr,'Ανάλυση των tweets (συναισθήματος, URL κ.ά.)...'
    outtweets = []
    partial_out_tweets = []
    for tweet in alltweets:
        tweet_date = tweet.created_at.date()
        tweet_text = tweet.text.encode('utf-8')
        
        # Ανάλυση συναισθήματος
        # Μετατροπή του tweet σε greeklish μικρά και σπάσιμό του σε λέξεις
        # για εύκολη σύγκριση με τις λέξεις του λεξικού
        words = unidecode(tweet_text.decode('utf-8')).lower().split()
        # Άθροιση του συνολικού συναισθήματος κάθε γνωστής λέξης από το λεξικό
        sentiment = sum(lexico.get(word, 0) for word in words)
        
        # Έλεγχος αν το tweet περιέχει url
        contains_url = 1 if 'http' in tweet_text else 0

        # Δημιουργία της τρέχουσας γραμμής για τα επιμέρους αρχεία χρήστη
        outtweets.append([tweet.id_str, tweet_text, tweet.created_at, tweet.retweet_count, tweet.favorite_count, sentiment, contains_url])
        
        # Δημιουργία της τρέχουσας μερικής γραμμής για το συνολικό αρχείο
        partial_out_tweets.append([tweet_date, tweet.retweet_count, tweet.favorite_count, sentiment, contains_url, screen_name])
        if tweet_date < min_date:
            min_date = tweet_date

    # Δημιουργία της τρέχουσας γραμμής με συνένωση των μερικών γραμμών, για το συνολικό αρχείο            
    combined_out_tweets.extend(partial_out_tweets)
    
    # Δημιουργία του εκάστοτε csv	
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        # Δημιουργία κεφαλίδων στηλών
        writer.writerow(['Αναγνωριστικό tweet','Κείμενο','Ημερομηνία δημιουργίας','Αριθμός retweets','Αριθμός αγαπημένων','Συναίσθημα','Περιέχει URL'])
        # Εγγραφή των tweets
        writer.writerows(outtweets)
  
    print 'Τα tweets εγγράφηκαν στο αρχείο %s_tweets.csv' % (screen_name)
    
    pass


if __name__ == '__main__':
    print '\033[92mΣΥΛΛΕΚΤΗΣ ΔΕΔΟΜΕΝΩΝ TWITTER 0.2\033[0m\nΒοήθεια: http://get-tweets.rtfd.io'
    for account in config['accounts']:
        print hr,'Έναρξη λήψης tweets για το λογαριασμό %s' % (account)
        get_all_tweets(account)
        print 'Η λήψη tweets για το λογαριασμό %s ολοκληρώθηκε' % (account)
    print hr,'Η λήψη tweets για όλους τους λογαριασμούς ολοκληρώθηκε' 
    
    # Δημιουργία του συνολικού csv	
    with open('combined_tweets.csv', 'wb') as f:
        writer = csv.writer(f)
        # Δημιουργία κεφαλίδων στηλών
        writer.writerow(['Ημερομηνία δημιουργίας','Αριθμός retweets','Αριθμός αγαπημένων','Συναίσθημα','Περιέχει URL','Χρήστης'])
        # Εγγραφή των tweets
        writer.writerows(combined_out_tweets)
    print hr,'Τα συνδυασμένα δεδομένα εγγράφηκαν στο αρχείο combined_tweets.csv'
    date_delta = max_date - min_date
    print 'Εύρος ημερομηνιών: από', min_date, 'μέχρι σήμερα (',date_delta,')'

    print hr,'Άθροιση δεδομένων...'
    final_tweets = []
    test_date = min_date
    while test_date <= max_date:

        # Αρχικοποίηση μεταβλητών και τρέχουσας γραμμής

        current_line = [test_date]
        for n, account in enumerate(config['accounts']):
            current_line.extend([0,0,0,0,0])
            
        for tweet in combined_out_tweets:
            if tweet[0] == test_date:
                for n, account in enumerate(config['accounts']):
                    if config['accounts'][n] == tweet[5]:
                        # άθροιση tweets n-οστού χρήστη
                        current_line[n * 5 + 1] += 1 
                        # άθροιση retweets n-οστού χρήστη
                        current_line[n * 5 + 2] += tweet[1]  
                        # άθροιση αγαπημένων n-οστού χρήστη
                        current_line[n * 5 + 3] += tweet[2] 
                        # άθροιση συναισθήματος n-οστού χρήστη
                        current_line[n * 5 + 4] += tweet[3] 
                        # άθροιση tweets με url n-οστού χρήστη
                        current_line[n * 5 + 5] += tweet[4] 

        final_tweets.append(current_line)
        test_date += timedelta(days=1)
    
    # Δημιουργία του τελικού csv	
    with open('final_tweets.csv', 'wb') as f:
        writer = csv.writer(f)
        # Δημιουργία κεφαλίδων στηλών
        header_line = ['Ημερομηνία']
        for n, account in enumerate(config['accounts']):
            header_line.extend(['Tweets '+account,'Retweets '+account,'Αγαπημένα '+account,'Συναίσθημα '+account,'Tweets με URL '+account])
        writer.writerow(header_line)
        # Εγγραφή των tweets
        writer.writerows(final_tweets)
    print 'Τα συγκεντρωτικά δεδομένα εγγράφηκαν στο αρχείο final_tweets.csv'
