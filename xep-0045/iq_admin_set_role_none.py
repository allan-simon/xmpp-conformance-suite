from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from config import ADMIN_NS
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

        #TODO: in current version of sleekxmpp (as of january 2014)
        # the setRole function is buggy, so we have to forge the iq ourself
        iq = self.makeIqSet()
        iq['to'] = ROOM_JID
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'item',
            {
                'role' : 'none',
                'nick'  : SECOND_BOT
            }
        )
        query.append(item)
        iq.append(query)

        try:
            stanza = iq.send()

        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        #self.disconnect()
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
            "muc::%s::got_offline" % ROOM_JID,
            self.participant_offline
        )


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
            wait=True
        )

if __name__ == '__main__':
    print_test_description(
        "An Admin set iq with role=none to a given nick  " +
        "should kick that user from current room ..."
    )


    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )

