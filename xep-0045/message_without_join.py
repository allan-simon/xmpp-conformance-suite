from sleekxmpp import ClientXMPP
from JoinMUCBot import JoinTestMUCBot

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from config import OWNER_BOT
from config import SECOND_BOT_JID
from config import ROOM_JID


ASK_SECOND_BOT_TO_SEND_MUC_MESSAGE = "try to send a muc message without joining"

class FirstBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("got_offline", self.got_offline)

    def got_offline(self, presence):
        # when the second disconnect we disconnect to
        if presence['from'].bare == SECOND_BOT_JID:
            self.disconnect()

    def participant_online(self, msg):
        # we arrive here when the group acknolwedge our presence
        # so at this step the group is existing
        # which is important, otherwise we will be in the case
        # "sending a message to a non existing group"
        if msg['muc'].getNick() == OWNER_BOT:
            # we tell the other bot, he can try to send a message
            self.send_message(
                mto=SECOND_BOT_JID,
                mbody=ASK_SECOND_BOT_TO_SEND_MUC_MESSAGE
            )
            return


class SecondBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("groupchat_message_error", self.group_message_error)

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

    def message(self, message):

        if message['body'] == ASK_SECOND_BOT_TO_SEND_MUC_MESSAGE:
            self.send_message(
                mto=ROOM_JID,
                mbody="whatever ",
                mtype='groupchat'
            )
    def group_message_error(self, message):
        if message['error']['condition'] == 'not-acceptable':
            print("[pass]")
        else:
            print('[fail]')

        self.disconnect()


if __name__ == '__main__':

    print_test_description(
        "If someone try to send a message to a group he's not part of " +
        "it should return a not-acceptable error ..."
    )

    init_test(
        class_first_bot = FirstBot,
        class_second_bot = SecondBot
    )
