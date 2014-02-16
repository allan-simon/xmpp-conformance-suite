from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from config import DISCO_INFO_NS
from config import ROOM_JID

from ConformanceUtils import init_test_one_bot
from ConformanceUtils import print_test_description

from JoinMUCBot import JoinTestMUCBot

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)

    def other_participant_online(self, msg):
        print("[fail]")
        self.disconnect()

    def self_online_in_muc(self, msg):
        iq = self.make_iq_get(
            queryxmlns=DISCO_INFO_NS,
            ito=ROOM_JID
        )

        try:
            stanza = iq.send(
                timeout=3
            )
            if (stanza['query'] == DISCO_INFO_NS):
                print("[pass]")
            else:
                print('[fail]')
        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    print_test_description(
        "An iq to a group, for disco info should success ..."
    )
    init_test_one_bot(EchoBot)
