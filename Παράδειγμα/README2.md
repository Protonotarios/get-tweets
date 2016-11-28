#Ανάλυση των αποτελεσμάτων

| :construction: ΥΠΟ ΚΑΤΑΣΚΕΥΗ :construction: |
| --- |

Η ανάλυση συναισθήματος με τεχνικές επεξεργασίας φυσικής γλώσσας γίνεται
με το πρόγραμμα **NiosTo** (βλ. [Acknowledgements](#Acknowledgements)

Το NiosTo δέχεται αρχεία `.xls` όπου το προς ανάλυση κείμενο πρέπει να βρίσκεται
στη δεύτερη στήλη. Η δεύτερη προϋπόθεση πληρούται καθώς τα εξαγόμενα `.csv` 
από το get-tweets.py έχουν το κείμενο των tweets στη δεύτερη στήλη.

Αυτό που μένει λοιπόν είναι να τα μετατρέψουμε σε `.xls`.

Ανοίγουμε ένα ένα τα αρχεία `.csv` με επεξεργαστή λογιστικών φύλλλων 
(π.χ. με το [LibreOffice Calc](https://el.libreoffice.org/)).

Κατά το άνοιγμα φροντίζουμε:
* η γλώσσα να είναι **Ελληνικά**,
* η κωδικοποίηση να είναι **UTF-8**, και
* το διαχωριστικό στηλών να είναι το **κόμμα** (`,`) και κανένα άλλο 
(αυτό είναι σημαντικό γιατί ορισμένα tweets περιέχουν ερωτηματικά ή άλλους
χαρακτήρες που χρησιμοποιούνται συνήθως ως διαχωριστικά).

## Acknowledgements

### NiosTo

Pantelis Agathangelou, Ioannis Katakis, Fotios Kokkoras, Konstantinos Ntonas
"Mining Domain-Specific Dictionaries of Opinion Words". In Proc. of the  15th
International Conference on Web Information System Engineering (WISE 2014),
Thessaloniki, Greece, 12-14 October, LNCS 8786, Springer, pp 47-62, 2014.
DOI: http://dx.doi.org/10.1007/978-3-319-11749-2_4

Free download for research or any other published work: http://deixto.com/niosto/