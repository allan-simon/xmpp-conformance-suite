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
            self.make_set_role_iq(name_type="jid", name="@").send()
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
