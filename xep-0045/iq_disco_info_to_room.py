from __future__ import print_function
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

from config import DISCO_INFO_NS

from ConformanceUtils import init_test_one_bot

class EchoBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.add_event_handler("session_start", self.session_start)

    def session_start(self, event):
        self.get_roster()
        self.send_presence()


        self.plugin['xep_0045'].joinMUC(
            "plop@conference.akario.local",
            self.nick,
            wait=True
        )


        iq = self.make_iq_get(
            queryxmlns=DISCO_INFO_NS,
            ito="plop@conference.akario.local"
        )

        print(
            "An iq to a group, for disco info should success ...",
            sep = ' ',
            end=''
        )

        try:
            stanza = iq.send(
                timeout=3
            )
            if (stanza['query'] == DISCO_INFO_NS):
                print("[pass]")
            else:
                print('[fail]')
        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    init_test_one_bot(EchoBot)
