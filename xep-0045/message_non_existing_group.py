from __future__ import print_function
from sleekxmpp import ClientXMPP

from config import ROOM_JID

from ConformanceUtils import init_test

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message_error", self.muc_message_error)

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.send_message(
            mto=ROOM_JID,
            mbody="Echo, from ",
            mtype='groupchat'
        )
        print(
            "A message to a MUC that does not exist should fail ...",
            sep = ' ',
            end=''
        )

    def muc_message_error(self, msg):
        #TODO add a more precise test
        print("[pass]")
        self.disconnect()


if __name__ == '__main__':
    init_test(
        number_of_bot = 1,
        class_first_bot = EchoBot
    )
