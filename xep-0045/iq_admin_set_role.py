from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET

from config import ADMIN_NS
from config import ROOM_JID
from config import SECOND_BOT

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from JoinMUCBot import JoinTestMUCBot

#TODO still need to add little more test to see if the set role
# is actually effective

class EchoBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )

        self.add_event_handler(
            "muc::%s::got_offline" % ROOM_JID,
            self.participant_offline
        )

    def participant_online(self, msg):
        if msg['muc'].getNick() != SECOND_BOT:
            return

        #TODO: in current version of sleekxmpp (as of january 2014)
        # the setRole function is buggy, so we have to forge the iq ourself
        iq = self.makeIqSet()
        iq['to'] = ROOM_JID
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'item',
            {
                'role' : 'moderator',
                'nick'  : SECOND_BOT
            }
        )
        query.append(item)
        iq.append(query)

        try:
            stanza = iq.send()
            print('[pass]')

        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        self.send_message(
            mto=ROOM_JID,
            mbody="disconnect %s" % SECOND_BOT,
            mtype='groupchat'
        )
        #self.disconnect()
    def participant_offline(self, presence):
        if presence['muc'].getNick() == SECOND_BOT:
            self.disconnect()
            return

class SecondBot(JoinTestMUCBot):

    def __init__(self, jid, password, nick):
        JoinTestMUCBot.__init__(self, jid, password, nick)
        self.add_event_handler("groupchat_message", self.muc_message)

    def muc_message(self, msg):
        if msg['body'] == 'disconnect %s' % SECOND_BOT:
            self.disconnect()


if __name__ == '__main__':
    print_test_description(
        "An Admin set iq with an existing role in item tag  " +
        "should return a 'result' iq ..."
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )
