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
* question_mark               -   Tweet enthält ein Fragezeichen
* is_wh_question              -   Ist eine W-Frage oder nicht

Abschließend: Alle Tweets löschen, die nicht Frage sind, Base-Tweet oder Antwort.

## Grundfragen

### Echo-Fragen
* Textähnlichkeit   [DONE]

### Wie werden Fragen beantwortet?
* Längere Dialoge = Mehr Fragen? 
* Wie oft werden Fragen beantwortet?
* Uhrzeit? 
* Anzahl Follower?  
* Zeitdifferenz zwischen Frage und Antwort  [DONE]
* Hypothese: Kurze Frage = Viele Antworten ('Hallo?'), mittlere Frage = wenig, lange Frage = Viele Antworten (echte Frage) [DONE]

