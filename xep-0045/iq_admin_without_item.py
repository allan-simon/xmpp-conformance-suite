from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from JoinMUCBot import JoinTestMUCBot

from config import SECOND_BOT
from config import SECOND_BOT_JID
from config import ROOM_JID

#TODO still need to add little more test to see if the set role
# is actually effective

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("got_offline", self.got_offline)

    def other_participant_online(self, msg):
        try:
            self.make_set_role_iq(childtag="NOT-ITEM", role="none").send()
            print("[fail]")
        except IqError as e:
            isCancel = e.iq['error']['type'] == 'cancel'
            isBadRequest = e.iq['error']['condition'] == 'bad-request'
            if  isCancel and isBadRequest :
                print("[pass]")
            else:
                print("[fail]")


        except IqTimeout:
            print("[fail]")


        self.send_message(
            mto=ROOM_JID,
            mbody="disconnect %s" % SECOND_BOT,
            mtype='groupchat'
        )

    def got_offline(self, presence):
        # when the second disconnect we disconnect to
        if presence['from'].bare == SECOND_BOT_JID:
            self.disconnect()


class SecondBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("groupchat_message", self.muc_message)

    def muc_message(self, msg):
        if msg['body'] == 'disconnect %s' % SECOND_BOT:
            self.disconnect()

if __name__ == '__main__':

    print_test_description(
        "An admin iq with something different than a 'item' tag as child " +
        "of query should return a bad-request error ..."
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )
