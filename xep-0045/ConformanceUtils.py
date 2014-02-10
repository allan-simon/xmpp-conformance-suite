'''
    Set of utils to quickly create test
'''

import logging
from config import SECOND_BOT
from config import SECOND_BOT_JID
from config import OWNER_BOT
from config import OWNER_BOT_JID
from config import BOT_PASSWORD

def TEST_PASSED ():
    print('[pass]')

def TEST_FAILED ():
    print('[fail]')


def init_test(
    number_of_bot = 2,
    class_first_bot = None,
    class_second_bot = None
):
    spawn_owner_bot(class_first_bot)

    if number_of_bot >= 2:
        spawn_second_bot(class_second_bot)

def init_test_one_bot(class_bot):
    init_test(
        number_of_bot=1,
        class_first_bot=class_bot
    )

def start_logging ():
    logging.basicConfig(
        level=logging.ERROR,
        format='%(levelname)-8s %(message)s'
    )


def spawn_muc_bot(bot_class, bot_jid, bot_password, bot_nick):

    xmpp = bot_class(bot_jid, bot_password, bot_nick)
    xmpp.register_plugin('xep_0045')

    #TODO: required only for disco related test
    xmpp.register_plugin('xep_0030')
    xmpp.connect()
    xmpp.process(block=False)


def spawn_owner_bot (OwnerBotClass):
    spawn_muc_bot(OwnerBotClass, OWNER_BOT_JID, BOT_PASSWORD, OWNER_BOT)

def spawn_second_bot (SecondBotClass):
    spawn_muc_bot(SecondBotClass, SECOND_BOT_JID, BOT_PASSWORD, SECOND_BOT)


