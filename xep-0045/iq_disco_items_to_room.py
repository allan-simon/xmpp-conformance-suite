from __future__ import print_function
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError
from sleekxmpp.exceptions import IqTimeout

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

        print(
            "An iq to a group, for disco items should success ...",
            sep = ' ',
            end=''
        )

        try:

            items = self['xep_0030'].get_items(
                jid="plop@conference.akario.local",
                block=True
            )
            print('[pass]')
            print(
                "an disco items iq to a group should return ourself...",
                sep=' ',
                end=''
            )
            discoItems = items['disco_items']['items']
            if (len(discoItems) == 1):
                for item in discoItems:
                    if (self.nick in item):
                        print('[pass]')
                    else:
                        print("[fail]")
            else:
                print("[fail]")
        except IqError as e:
            print("[fail]")
        except IqTimeout:
            print("[fail]")

        self.disconnect()

if __name__ == '__main__':
    init_test_one_bot(EchoBot)
