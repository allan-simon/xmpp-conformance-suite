from __future__ import print_function

from ConformanceUtils import init_test_one_bot
from ConformanceUtils import spawn_muc_bot

from config import ROOM_JID
from config import SECOND_BOT_JID
from config import OWNER_BOT

from JoinMUCBot import JoinTestMUCBot

TRY_SEND_MESSAGE = "try send message"
FORBIDDEN_MESSAGE = "nobody allow me to talk"

#TODO echo bot tell second bot that now he can try to send a message
# second bot send a message => should get "forbidden"

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("got_offline", self.got_offline)


    def got_offline(self, presence):
        # when the second disconnect we disconnect to
        if presence['from'].bare == SECOND_BOT_JID:
            self.disconnect()


class SecondBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("groupchat_message_error", self.muc_message_error)
        self.add_event_handler("groupchat_presence", self.groupchat_presence)


    def groupchat_presence(self, presence):

        conflictFrom = "%s/%s" % (ROOM_JID, OWNER_BOT)

        # TODO: to make the test more precise we should check that the error
        # code is 409 conflict
        if presence['type'] == 'error' and presence['from'] == conflictFrom:
            print("[pass]")
            self.disconnect()

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
        print('[fail]')
        self.disconnect()


if __name__ == '__main__':

    print(
        "If a room participant with role visitor try to send a message " +
        "it should return a message error forbidden ..." ,
        sep = ' ',
        end=''
    )

    init_test_one_bot(EchoBot)
    spawn_muc_bot(SecondBot, SECOND_BOT_JID, 'plop', OWNER_BOT)
