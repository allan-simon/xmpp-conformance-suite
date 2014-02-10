from __future__ import print_function

from JoinMUCBot import JoinTestMUCBot

from ConformanceUtils import init_test

from config import ROOM_JID
from config import SECOND_BOT
TRY_SEND_MESSAGE = "try send message"
FORBIDDEN_MESSAGE = "nobody allow me to talk"

#TODO echo bot tell second bot that now he can try to send a message
# second bot send a message => should get "forbidden"

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )

        self.add_event_handler(
            "muc::%s::got_offline" % ROOM_JID,
            self.participant_offline
        )

    def participant_online(self, msg):
        if msg['muc'].getNick() != SECOND_BOT:
            return

        self.plugin['xep_0045'].setRole(
            ROOM_JID,
            SECOND_BOT,
            'visitor'
        )

        self.send_message(
            mto=ROOM_JID,
            mbody=TRY_SEND_MESSAGE,
            mtype='groupchat'
        )

    def participant_offline(self, presence):
        if presence['muc'].getNick() == SECOND_BOT:
            self.disconnect()
            return

class SecondBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("groupchat_message_error", self.muc_message_error)

    def muc_message(self, msg):
        if msg['body'] == TRY_SEND_MESSAGE:

            self.send_message(
                mto=ROOM_JID,
                mbody=FORBIDDEN_MESSAGE,
                mtype='groupchat'
            )

        # if we arrive here it means the previous
        # message has been accepted, which is not
        # excepted...
        if msg['body'] == FORBIDDEN_MESSAGE:
            print('[fail]')
            self.disconnect()

    def muc_message_error(self, msg):
        print('[pass]')
        self.disconnect()


if __name__ == '__main__':
    print(
        "If a room participant with role visitor try to send a message " +
        "it should return a message error forbidden ..." ,
        sep = ' ',
        end=''
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )
