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
        item = ET.Element(
            'item',
            {'role' : 'moderator'}
        )
        query.append(item)
        iq.append(query)

        print(
            "a admin get iq to get all occupants with role " +
            " 'moderator',should succeed if made by one of the moderator  ..." ,
            sep = ' ',
            end=''
        )

        try:
            stanza = iq.send()
            #TODO make a more in-depth test, it's supposed
            #to return the list of owner (i.e at least current nick)
            query = stanza.xml.find('{%s}query' % ADMIN_NS)
            if query is not None:
                item = query.find('{%s}item' % ADMIN_NS)
                if item.attrib['role'] == 'moderator':
                    print('[pass]')
                else:
                    print('[fail]')
            else:
                print('[fail]')

        except IqError as e:
            print('[fail]')
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    init_test_one_bot(EchoBot)
