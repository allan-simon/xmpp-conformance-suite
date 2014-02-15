from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET

from ConformanceUtils import init_test_one_bot
from ConformanceUtils import print_test_description

from config import ADMIN_NS
from config import ROOM_JID

from JoinMUCBot import JoinTestMUCBot

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )

    def participant_online(self, msg):
        if msg['muc'].getNick() != self.nick:
            print("[fail]")
            self.disconnect()
            return

        iq = self.makeIqGet()
        iq['to'] = "plop@conference.akario.local"
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'item',
            {'affiliation' : 'owner'}
        )
        query.append(item)
        iq.append(query)

        try:
            stanza = iq.send()
            #TODO make a more in-depth test, it's supposed
            #to return the list of owner (i.e at least current nick)
            if (stanza['query'] == ADMIN_NS):
                print('[pass]')
            else:
                print('[fail]')
        except IqError as e:
            print('[fail]')
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    print_test_description(
        "a admin get iq to get all occupants with affiliation " +
        " 'owner',should succeed if made by the owner  ..."
    )

    init_test_one_bot(EchoBot)
