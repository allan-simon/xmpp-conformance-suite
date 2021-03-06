from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

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
            self.make_admin_get_iq(key="not-role-not-affiliation").send()
        except IqError as e:
            if (e.iq['error']['type'] == 'cancel'):
                print("[pass]")
            else:
                print['[fail]']
        except IqTimeout:
            print("[fail]")

        self.disconnect()


if __name__ == '__main__':
    print_test_description(
        "If an admin get iq contain an item with neither " +
        "affiliation nor role, it must return an error iq ..."
    )

    init_test_one_bot(EchoBot)
