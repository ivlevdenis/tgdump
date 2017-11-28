Установка
==========

`sudo apt install virtualenv`

`git clone https://bitbucket.org/nadirstream/telemachina.git` 

`cd tgdump` 

`chmod a+x tgdump` 

python3.5 

`virtualenv -p python3.5 venv` 

python3.6 

`virtualenv -p python3.6 venv` 

`source venv/bin/activate`

`pip install -r requirements.txt`

Использование
==============
`cd PATH/TO/tgdump`

`source venv/bin/activate`

`./tgdump --help`

```
usage: tgdump [-h] --entities ENTITIES [--output OUTPUT] [--phone PHONE]
              [--api-id API_ID] [--api-hash API_HASH] [--session SESSION]
              [--senders SENDERS] [--limit LIMIT] [--offset-date OFFSET_DATE]
              [--offset-id OFFSET_ID] [--max-id MAX_ID] [--min-id MIN_ID]

Dump Telegram messages. Suports User, Chat, Channel peers. ATTENTION! Do not
support pipes!

optional arguments:
  -h, --help            show this help message and exit
  --entities ENTITIES   Comma separated list of entities or filename. Support
                        phone (string statrted with '+'), username (started
                        with '@'), or integer ID for chats or channel.
  --output OUTPUT       Output JSON filename.
  --phone PHONE         International format phone number '+79998887766'. If
                        not specified, the environment variable PHONE is used.
  --api-id API_ID       API_ID can get by link my.telegram.org/apps. If not
                        specified, the environment variable API_ID is used.
  --api-hash API_HASH   API_HASH can get by link my.telegram.org/apps. If not
                        specified, the environment variable API_HASH is used.
  --session SESSION     Name of session, used for session filename, If not
                        specified, used teporary session.
  --senders SENDERS     If specified, then include serder info to 'peer' as
                        'meta' param.
  --limit LIMIT         Number of messages to be retrieved. Due to limitations
                        with the API retrieving more than 3000 messages will
                        take longer than half a minute (or even more based on
                        previous calls). The limit may also be None, which
                        would eventually return the whole history.
  --offset-date OFFSET_DATE
                        Offset date (messages *previous* to this date will be
                        retrieved). Example 01.01.2017.
  --offset-id OFFSET_ID
                        Offset message ID (only messages *previous* to the
                        given ID will be retrieved).
  --max-id MAX_ID       All the messages with a higher (newer) ID or equal to
                        this will be excluded.
  --min-id MIN_ID       All the messages with a lower (older) ID or equal to
                        this will be excluded.
```