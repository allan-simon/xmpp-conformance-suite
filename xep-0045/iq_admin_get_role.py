from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

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

        try:
            stanza = self.make_admin_get_iq().send()
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

    print_test_description(
        "a admin get iq to get all occupants with role " +
        " 'moderator',should succeed if made by one of the moderator  ..."
    )
    init_test_one_bot(EchoBot)
