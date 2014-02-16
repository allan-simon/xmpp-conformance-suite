from sleekxmpp import ClientXMPP

from config import ROOM_JID
from config import ADMIN_NS
from config import SECOND_BOT

from sleekxmpp.xmlstream import ET

class JoinTestMUCBot(ClientXMPP):

    def __init__(self, jid, password, nick):
        ClientXMPP.__init__(self, jid, password)
        self.nick = nick
        self.room_jid = ROOM_JID
        self.add_event_handler("session_start", self.session_start)

        self.add_event_handler(
            "muc::%s::got_online" % ROOM_JID,
            self.participant_online
        )


    def participant_online(self, msg):
        pass

    def make_set_role_iq(
        self,
        role="moderator",
        childtag="item",
        name_type="nick",
        name=SECOND_BOT
    ):

        #TODO: in current version of sleekxmpp (as of january 2014)
        # the setRole function is buggy, so we have to forge the iq ourself
        iq = self.makeIqSet()
        iq['to'] = ROOM_JID
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            childtag,
            {
                'role' : role,
                name_type  : name
            }
        )
        query.append(item)
        iq.append(query)
        return iq

    def make_admin_get_iq(
        self,
        key="role",
        value="moderator"
    ):
        #TODO: can be replaced by a getRole function I suppose
        iq = self.makeIqGet()
        iq['to'] = ROOM_JID
        query = ET.Element('{%s}query' % ADMIN_NS)
        item = ET.Element(
            'item',
            {key : value}
        )
        query.append(item)
        iq.append(query)
        return iq



    def session_start(self, event):
        self.get_roster()
        self.send_presence()

        self.plugin['xep_0045'].joinMUC(
            self.room_jid,
            self.nick,
            wait=True
        )

