from __future__ import print_function
import logging
from sleekxmpp import ClientXMPP

ROOM_JID = "plop@conference.akario.local"
SECOND_BOT_JID = "psi@akario.local"
OWNER_BOT_JID = "allan@akario.local"
SECOND_BOT = "bot_2"
OWNER_BOT = "bot_1"
ASK_SECOND_BOT_TO_SEND_MUC_MESSAGE = "try to send a muc message without joining"

class FirstBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("got_offline", self.got_offline)

        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            wait=True
        )

    def got_offline(self, presence):
        # when the second disconnect we disconnect to
        if presence['from'].bare == SECOND_BOT_JID:
            self.disconnect()

    def participant_online(self, msg):
        # we arrive here when the group acknolwedge our presence
        # so at this step the group is existing
        # which is important, otherwise we will be in the case
        # "sending a message to a non existing group"
        if msg['muc'].getNick() == OWNER_BOT:
            # we tell the other bot, he can try to send a message
            self.send_message(
                mto=SECOND_BOT_JID,
                mbody=ASK_SECOND_BOT_TO_SEND_MUC_MESSAGE
            )
            return


class SecondBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_message_error", self.group_message_error)

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

    def message(self, message):

        if message['body'] == ASK_SECOND_BOT_TO_SEND_MUC_MESSAGE:
            self.send_message(
                mto=ROOM_JID,
                mbody="whatever ",
                mtype='groupchat'
            )
    def group_message_error(self, message):
        if message['error']['condition'] == 'not-acceptable':
            print("[pass]")
        else:
            print('[fail]')

        self.disconnect()




if __name__ == '__main__':
    logging.basicConfig(
        level=logging.ERROR,
        format='%(levelname)-8s %(message)s'
    )


    print(
        "If someone try to send a message to a group he's not part of " +
        "it should return a not-acceptable error ..." ,
        sep = ' ',
        end=''
    )

    xmpp = FirstBot(OWNER_BOT_JID, 'plop', OWNER_BOT)
    xmpp.register_plugin('xep_0045')
    xmpp.connect()
    xmpp.process(block=False)

    xmpp2 = SecondBot(SECOND_BOT_JID, 'plop', SECOND_BOT)
    xmpp2.register_plugin('xep_0045')
    xmpp2.connect()
    xmpp2.process(block=False)
