from __future__ import print_function
import logging
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from sleekxmpp.xmlstream import ET
ADMIN_NS = "http://jabber.org/protocol/muc#admin"
SECOND_BOT_JID = "psi@akario.local"
ROOM_JID = "plop@conference.akario.local"
SECOND_BOT = "bot_2"

#TODO still need to add little more test to see if the set role
# is actually effective

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )
        self.add_event_handler("got_offline", self.got_offline)

    def participant_online(self, msg):
        if msg['muc'].getNick() != SECOND_BOT:
            return

        #TODO: in current version of sleekxmpp (as of january 2014)
        # the setRole function is buggy, so we have to forge the iq ourself
        iq = self.makeIqSet()
        iq['to'] = ROOM_JID
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'NOT-ITEM',  # on purpose to trigger the error
            {
                'role' : 'none',
                'nick'  : SECOND_BOT
            }
        )
        query.append(item)
        iq.append(query)



        try:
            iq.send()
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


    def muc_message(self, msg):
        if msg['body'] == 'disconnect %s' % SECOND_BOT:
            self.disconnect()

    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].joinMUC(
            ROOM_JID,
            self.nick,
            wait=True
        )

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.ERROR,
        format='%(levelname)-8s %(message)s'
    )

    print(
        "An admin iq with something different than a 'item' tag as child " +
        "of query should return a bad-request error ..." ,
        sep = ' ',
        end=''
    )

    xmpp = EchoBot('allan@akario.local', 'plop', "bot_1")
    xmpp.register_plugin('xep_0045')
    xmpp.connect()
    xmpp.process(block=False)

    xmpp2 = SecondBot('psi@akario.local', 'plop', SECOND_BOT)
    xmpp2.register_plugin('xep_0045')
    xmpp2.connect()
    xmpp2.process(block=False)