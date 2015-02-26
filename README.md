# TwitterDialogs

## Datenbank-Layout

### Direkt beim Einlesen
* id_str                      -   Status ID
* user_id_str                 -   ID des Users
* friend_count                -   Anzahl der User, denen der Autor folgt
* followers_count             -   Anzahl der User, die dem Autor folgen
* in_reply_to_status_id_str   -   Antwort auf Tweet
* in_reply_to_user_id_str     -   Antwort auf User
* user_mentions_count         -   Anzahl der User, die im Tweet erwähnt werden
* user_mentions               -   Liste von UserIDs, die im Tweet erwähnt werden ("ID","ID"...)
* created_at                  -   Zeitpunkt des Erstellens
* source                      -   Client, mit dem Tweet verfasst wurde
* text                        -   Inhalt des Tweets

### Erfordern Nachbereitung
* direct_replies_count        -   Anzahl Tweets, die direkt auf den Tweet antworten
* direct_replies              -   Liste von TweetIDs, die direkt auf den Tweet antworten
* indirect_replies_count      -   Anzahl Tweets, die direkt oder indirekt auf den Tweet antworten
* indirect_replies            -   Liste von TweetIDs, die direkt oder indirekt auf den Tweet antworten
* is_base_tweet               -   Tweet startet Dialog (ist keine Antwort!)

* is_question                 -   Tweet ist eine Frage (muss aber keine Antworten haben)
* question_mark_counter       -   Number of Questionmarks
* is_wh_question              -   Ist eine W-Frage oder nicht

Abschließend: Alle Tweets löschen, die nicht Frage sind, Base-Tweet oder Antwort.

## Todo
* Datetime-Objekt parsen
* Struktur für MySQL
* 'Basis-Tweets' finden
* Fragen identifizieren!
* Längere Dialoge = Mehr Fragen?


## Grundklassen
* Dialog-Tree
* MySQL Zugriff
* Dialog-Iterator
* Suchfunktionen
* IDs auflösen

## Grundfragen

### Echo-Fragen
* Textähnlichkeit

### Wie werden Fragen beantwortet?
* Wie oft werden Fragen beantwortet?
* Uhrzeit?
* Anzahl Follower?
* Zeitdifferenz zwischen Frage und Antwort
* Hypothese: Kurze Frage = Viele Antworten ('Hallo?'), mittlere Frage = wenig, lange Frage = Viele Antworten (echte Frage)

### Intonation bei Fragen auf Twitter
* Suchmuster
* Ratio Groß/Kleinbuchstaben
* Längere Sequenz von Großbuchstaben
* Sequenz von nicht-Buchstaben
* Emoticons?
