from __future__ import print_function
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from ConformanceUtils import init_test

from config import OWNER_BOT
from config import SECOND_BOT
from config import ROOM_JID

#TODO still need to add little more test to see if the set role
# is actually effective

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler(
            "muc::%s::got_offline" % ROOM_JID,
            self.participant_offline
        )

    def participant_offline(self, presence):
        if presence['muc'].getNick() == SECOND_BOT:
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

        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )

        self.add_event_handler(
            "muc::%s::got_offline" % ROOM_JID,
            self.participant_offline
        )

    def participant_online(self, msg):

        if msg['muc'].getNick() == OWNER_BOT:
            # we try to set the owner as simple 'participant'
            try:
                self.plugin['xep_0045'].setRole(
                    ROOM_JID,
                    OWNER_BOT,
                    'participant'
                )
            except IqError as e:
                if e.iq['error']['condition'] == 'not-allowed':
                    print('[pass]')
                else:
                    print('[fail]')
            except IqTimeout:
                print("[fail]")

            self.disconnect()

    def participant_offline(self, presence):
        # if we receive a "offline" from ourself
        # it means we've been kicked
        if presence['muc'].getNick() == self.nick:

            print('[pass]')
            self.disconnect()

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            OWNER_BOT
        )

if __name__ == '__main__':
    print(
        "If a non owner/admin moderator try to change the role of the owner " +
        "it should return a not-allowed error ..." ,
        sep = ' ',
        end=''
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )
