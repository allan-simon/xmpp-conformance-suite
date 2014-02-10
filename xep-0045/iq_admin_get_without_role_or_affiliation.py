from __future__ import print_function
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET
from config import ADMIN_NS

from ConformanceUtils import init_test_one_bot

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

        iq = self.makeIqGet()
        iq['to'] = "plop@conference.akario.local"
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element('item')
        query.append(item)
        iq.append(query)

        print(
            "If an admin get iq contain an item with neither " +
            "affiliation nor role, it must return an error iq ..." ,
            sep = ' ',
            end=''
        )

        try:
            iq.send()
        except IqError as e:
            if (e.iq['error']['type'] == 'cancel'):
                print("[pass]")
            else:
                print['[fail]']
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    init_test_one_bot(EchoBot)
