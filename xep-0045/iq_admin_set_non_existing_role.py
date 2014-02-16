from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET

from config import ADMIN_NS
from config import SECOND_BOT
from config import ROOM_JID

from ConformanceUtils import init_test
from ConformanceUtils import print_test_description

from JoinMUCBot import JoinTestMUCBot

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

        iq = self.makeIqSet()
        iq['to'] = ROOM_JID
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'item',
            {
                'role' : 'non-existing',
                'nick'  : SECOND_BOT
            }
        )
        query.append(item)
        iq.append(query)

        try:
            stanza = iq.send()
            print('[fail]')

        except IqError as e:
            if e.iq['error']['type'] == 'modify' and e.iq['error']['condition'] == 'not-acceptable' :
                print('[pass]')
            else:
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
        "An Admin set iq with a non existing role in item tag  " +
        "should return a not-acceptable error ..."
    )

    init_test(
        class_first_bot = EchoBot,
        class_second_bot = SecondBot
    )
