from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

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
        try:

            items = self['xep_0030'].get_items(
                jid=ROOM_JID,
                block=True
            )

            discoItems = items['disco_items']['items']
            if (len(discoItems) == 1):
                for item in discoItems:
                    if (self.nick in item):
                        print('[pass]')
                    else:
                        print("[fail]")
            else:
                print("[fail]")
        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    print_test_description(
        "An iq to a group, for disco items should success and " +
        " return ourself..."
    )
    init_test_one_bot(EchoBot)
