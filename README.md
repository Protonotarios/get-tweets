# Συλλέκτης δεδομένων από το Twitter

Το πρόγραμμα συλλέγει τα πλήρη στοιχεία ενός συνόλου λογαριασμών 
του Twitter που εμείς ορίζουμε καθώς και όλα τα tweets αυτών των
λογαριασμών και τα αποθηκεύει σε αρχεία `.csv`.

Το πρόγραμμα είναι στα Ελληνικά.

| :construction: ΥΠΟ ΚΑΤΑΣΚΕΥΗ :construction: |
| --- |

## Χρήση του προγράμματος

### Προαπαιτούμενα

1. Αρχικά δημιουργούμε τα απαραίτητα API credentials στο Twitter στη 
διεύθυνση: https://apps.twitter.com/app/new

2. Στη συνέχεια περνάμε τα διαπιστευτήρια στο αρχείο [config.py](config.py)

3. Στο ίδιο αρχείο περνάμε τα usernames των λογαριασμών Twitter που
θέλουμε να συλλέξουμε.

4. Για να τρέξει το πρόγραμμα χρειάζεται τη βιβλιοθήκη [tweepy](https://github.com/tweepy/tweepy). 
Εγκαθιστούμε τη βιβλιοθήκη με
```
pip install tweepy
```
	
### Εκτέλεση

Εκτελούμε το πρόγραμμα [get-user-data.py](get-user-data.py) το οποίο 
συλλέγει τα στοιχεία (μεταδεδομένα) των λογαριασμών που έχουμε ορίσει
και τα αποθηκεύει στο αρχείο `user data.csv`.

Στη συνέχεια εκτελούμε το πρόγραμμα [get-tweets.py](get-tweets.py) το 
οποίο δημιουργεί 3 αρχεία `.csv` που περιέχουν όλα τα tweets των λογαριασμών
καθώς και κάποια μεταδεδομένα των tweets όπως αριθμός retweets, αριθμός likes κ.ά.

Αποθηκεύει επίσης και τις εικόνες προφίλ των λογαριασμών.

Να σημειωθεί ότι το Twitter έχει δύο περιορισμούς όσον αφορά στη χρήση του API:

1. Σε κάθε αίτημα επιτρέπει τη λήψη μέχρι και 200 tweets.
2. Συνολικά επιτρέπει τη λήψη των 3240 πιο πρόσφατων tweets από κάθε λογαριασμό.

Αυτό σημαίνει ότι τα tweets λαμβάνονται ανά διακοσάδες και ότι ο μέγιστος
αριθμός tweets που μπορούμε να λάβουμε για έναν λογαριασμό είναι 3240.

Ένα ενδεικτικό παράδειγμα χρήσης μπορείτε να δείτε στο φάκελο [Παράδειγμα](Παράδειγμα).

## Acknowledgements

* [get-tweets.py]() is based on yanofsky's gist [tweet_dumper.py](https://gist.github.com/yanofsky/5436496)
* Ο σχεδιασμός της φιλοσοφίας του προγράμματος έγινε σε συνεργασία με τη 
Βάνα Σαρήμπεη η οποία έκανε και το beta testing και εντόπισε τα bugs.

## License

[MIT](LICENSE)