from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from config import OWNER_BOT
from config import SECOND_BOT
from config import ROOM_JID

from JoinMUCBot import JoinTestMUCBot

#TODO still need to add little more test to see if the set role
# is actually effective

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)

    def participant_offline(self, presence):
        if presence['muc'].getNick() == SECOND_BOT:
            self.disconnect()


class SecondBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)

    def participant_online(self, msg):

        if msg['muc'].getNick() == OWNER_BOT:
            # we try to set the owner as simple 'participant'
            try:
                self.plugin['xep_0045'].setRole(
                    ROOM_JID,
                    OWNER_BOT,
                    'participant'
                )
            except IqError as e:
                if e.iq['error']['condition'] == 'not-allowed':
                    print('[pass]')
                else:
                    print('[fail]')
            except IqTimeout:
                print("[fail]")

            self.disconnect()

    def participant_offline(self, presence):
        # if we receive a "offline" from ourself
        # it means we've been kicked
        if presence['muc'].getNick() == self.nick:

            print('[pass]')
            self.disconnect()


if __name__ == '__main__':
    print_test_description(
        "If a non owner/admin moderator try to change the role of the owner " +
        "it should return a not-allowed error ..."
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )
