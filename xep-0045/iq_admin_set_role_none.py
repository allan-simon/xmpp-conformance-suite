from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from config import SECOND_BOT
from config import ROOM_JID

from JoinMUCBot import JoinTestMUCBot

#TODO still need to add little more test to see if the set role
# is actually effective

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)

    def other_participant_online(self, msg):
        try:
            self.make_set_role_iq(role="none").send()

        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        #self.disconnect()
    def participant_offline(self, presence):
        if presence['muc'].getNick() == SECOND_BOT:
            self.disconnect()

class SecondBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)

    def participant_offline(self, presence):
        # if we receive a "offline" from ourself
        # it means we've been kicked
        if presence['muc'].getNick() == self.nick:

            print('[pass]')
            self.disconnect()

if __name__ == '__main__':
    print_test_description(
        "An Admin set iq with role=none to a given nick  " +
        "should kick that user from current room ..."
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )

