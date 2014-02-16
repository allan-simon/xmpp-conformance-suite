from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from ConformanceUtils import init_test_one_bot
from ConformanceUtils import print_test_description

from config import ADMIN_NS
from config import ROOM_JID

from JoinMUCBot import JoinTestMUCBot

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)

    def other_participant_online(self, msg):
        print("[fail]")
        self.disconnect()

    def self_online_in_muc(self, msg):

        try:
            stanza = self.make_admin_get_iq(
                key="affiliation",
                value="owner"
            ).send()
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
