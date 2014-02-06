from __future__ import print_function
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET
ADMIN_NS = "http://jabber.org/protocol/muc#admin"

ROOM_JID = "plop@conference.akario.local"
SECOND_BOT = "bot_2"

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )

        self.add_event_handler(
            "muc::%s::got_offline" % ROOM_JID,
            self.participant_offline
        )

    def participant_online(self, msg):
        print(self.nick +": oh a presence")
        if msg['muc'].getNick() != SECOND_BOT:
            return
        print(msg['muc'].getNick())

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

        print(
            "An Admin set iq with a malformed jid attribute in item tag  " +
            "should return a jid-malformed error ..." ,
            sep = ' ',
            end=''
        )

        try:
            stanza = iq.send()
            print(stanza)
            print('plop[fail]')

        except IqError as e:
            if e.iq['error']['condition'] == 'jid-malformed':
                print('[pass]')
            else:
                print(e.iq)
                print('errr[fail]')
        except IqTimeout:
            print("timeout[fail]")

        print("send message")
        self.send_message(
            mto=ROOM_JID,
            mbody="disconnect %s" % SECOND_BOT,
            mtype='groupchat'
        )
        #self.disconnect()
    def participant_offline(self, presence):
        if presence['muc'].getNick() == SECOND_BOT:
            print("bye %s" % self.nick)
            self.disconnect()
            return





    def session_start(self, event):
        self.get_roster()
        self.send_presence()


        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            wait=True
        )
class SecondBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message", self.muc_message)


    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            wait=True
        )

    def muc_message(self, msg):
        print("prouuuuut")
        print(msg['mucnick'])
        if msg['body'] == 'disconnect %s' % SECOND_BOT:
            print("bye %s" % self.nick)
            self.disconnect()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.ERROR,
        format='%(levelname)-8s %(message)s'
    )

    xmpp = EchoBot('allan@akario.local', 'plop', "bot_1")
    xmpp.register_plugin('xep_0045')
    xmpp.connect()
    xmpp.process(block=False)

    xmpp2 = SecondBot('psi@akario.local', 'plop', SECOND_BOT)
    xmpp2.register_plugin('xep_0045')
    xmpp2.connect()
    xmpp2.process(block=False)
