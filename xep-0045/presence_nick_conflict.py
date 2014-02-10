from __future__ import print_function
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET
ADMIN_NS = "http://jabber.org/protocol/muc#admin"

ROOM_JID = "plop@conference.akario.local"
SECOND_BOT_JID = "psi@akario.local"
SECOND_BOT = "bot_2"
TRY_SEND_MESSAGE = "try send message"
FORBIDDEN_MESSAGE = "nobody allow me to talk"

#TODO echo bot tell second bot that now he can try to send a message
# second bot send a message => should get "forbidden"

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("got_offline", self.got_offline)


    def got_offline(self, presence):
        # when the second disconnect we disconnect to
        if presence['from'].bare == SECOND_BOT_JID:
            self.disconnect()




    def session_start(self, event):
        self.get_roster()
        self.send_presence()


        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            wait=True
        )
class SecondBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("groupchat_message_error", self.muc_message_error)
        self.add_event_handler("groupchat_presence", self.groupchat_presence)


    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            wait=True
        )

    def groupchat_presence(self, presence):

        conflictFrom = "%s/%s" % (ROOM_JID, SECOND_BOT)

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
    logging.basicConfig(
        level=logging.ERROR,
        format='%(levelname)-8s %(message)s'
    )

    print(
        "If a room participant with role visitor try to send a message " +
        "it should return a message error forbidden ..." ,
        sep = ' ',
        end=''
    )

    xmpp = EchoBot('allan@akario.local', 'plop', SECOND_BOT)
    xmpp.register_plugin('xep_0045')
    xmpp.connect()
    xmpp.process(block=False)

    xmpp2 = SecondBot(SECOND_BOT_JID, 'plop', SECOND_BOT)
    xmpp2.register_plugin('xep_0045')
    xmpp2.connect()
    xmpp2.process(block=False)
