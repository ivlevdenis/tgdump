from time import sleep
from operator import itemgetter
from telethon import TelegramClient as BaseTelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import PeerChat, PeerUser, PeerChannel
from telethon.tl.functions.messages import GetDialogsRequest

NEED_PASSWORD = 101
NOT_AUTORIZE = 201


class TelegramClient(object):
    clients = {}

    def __init__(self, session, phone, api_id, api_hash):
        if isinstance(phone, str):
            if phone.startswith('+'):
                phone = int(phone[1:])
        self.session = session
        self.phone = phone
        self.api_id = api_id
        self.api_hash = api_hash
        self.authorized = False

        self.client = BaseTelegramClient(
            self.session,
            self.api_id,
            self.api_hash,
        )
        self.client.connect()

    def authorize(self):
        if not self.client.is_user_authorized():
            self.client.send_code_request(self.phone)
            return False
        return True

    def sign_in_code(self, code):
        try:
            self.client.sign_in(phone=self.phone, code=code)
        except SessionPasswordNeededError:
            return NEED_PASSWORD
        else:
            self.authorized = True

    def sign_in_password(self, password):
        self.client.sign_in(phone=self.phone, password=password)

    def dialogs(self):
        dialogs, entities = self.client.get_dialogs(limit=100)
        _entities = (e.to_dict() for e in entities)
        entities = {e['id']: e for e in _entities}
        dialogs = [d.to_dict() for d in dialogs]
        dialogs.sort(key=itemgetter('top_message'), reverse=True)

        for d in dialogs:
            if 'user_id' in d['peer']:
                d['peer'].update({
                    'meta': entities[d['peer']['user_id']]
                })
            elif 'chat_id' in d['peer']:
                d['peer'].update({
                    'meta': entities[d['peer']['chat_id']]
                })
            elif 'channel_id' in d['peer']:
                d['peer'].update({
                    'meta': entities[d['peer']['channel_id']]
                })

        return {'dialogs': dialogs}

    def messages(self,
                 entity_id,
                 limit=20,
                 offset_date=None,
                 offset_id=0,
                 max_id=0,
                 min_id=0):
        if isinstance(entity_id, str) and entity_id.startswith('@') or entity_id.startswith('+'):
            entity = self.client.get_entity(entity_id)
        else:
            try:
                entity = self.client.get_entity(PeerUser(int(entity_id)))
            except ValueError:
                try:
                    entity = self.client.get_entity(PeerChat(int(entity_id)))
                except ValueError:
                    entity = self.client.get_entity(
                        PeerChannel(int(entity_id))
                    )
        count, messages, senders = self.client.get_message_history(
            entity,
            limit=limit,
            offset_date=offset_date,
            offset_id=offset_id,
            max_id=max_id,
            min_id=min_id,
        )
        messages = [m.to_dict() for m in messages]
        # ToDo: Fix media!
        for m in messages:
            if 'media' in m and m['media']:
                m.update({'media': None})

        _senders = (s.to_dict() for s in senders)
        senders = {s['id']: s for s in _senders}

        messages.sort(key=itemgetter('date'), reverse=False)
        return {'count': count, 'messages': messages, 'senders': senders}

    def send_message(self, entity_id, message):
        message = self.client.send_message(int(entity_id), message)
        return {'message': message.to_dict()}
