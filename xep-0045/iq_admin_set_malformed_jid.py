from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET

from config import ADMIN_NS
from config import ROOM_JID

from ConformanceUtils import init_test_one_bot
from ConformanceUtils import print_test_description

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)

    def session_start(self, event):
        self.get_roster()
        self.send_presence()


        self.plugin['xep_0045'].joinMUC(
            "plop@conference.akario.local",
            self.nick,
            wait=True
        )

        iq = self.makeIqSet()
        iq['to'] = "plop@conference.akario.local"
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'item',
            {
                'role' : 'moderator',
                'jid'  : '@'
            }
        )
        query.append(item)
        iq.append(query)

        try:
            stanza = iq.send()
            print('[fail]')

        except IqError as e:
            if e.iq['error']['condition'] == 'jid-malformed':
                print('[pass]')
            else:
                print('[fail]')
        except IqTimeout:
            print("[fail]")
        self.disconnect()

if __name__ == '__main__':
    print_test_description(
        "An Admin set iq with a malformed jid attribute in item tag  " +
        "should return a jid-malformed error ..."
    )

    init_test_one_bot(EchoBot)
