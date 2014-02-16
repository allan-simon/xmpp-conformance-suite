from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET

from config import ADMIN_NS
from config import ROOM_JID

from ConformanceUtils import init_test_one_bot
from ConformanceUtils import print_test_description

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

        iq = self.makeIqSet()
        iq['to'] = ROOM_JID
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
