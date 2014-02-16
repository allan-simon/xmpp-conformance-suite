from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

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
