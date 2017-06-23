#!/usr/bin/python3.5


from source.baseclass.card import Card
# from source.baseclass.globalvar import GlobalVar

ERROR_CARDSEED_FAILED = 'Seed failed  Reason:{} '


class CardT10xx(Card):

    def __init__(self, options):
        super(Card, self).__init__(options)

    def do_getbid(self):
        self.session_telnet.login()
        self.do_getbid_t10xx(self.session_telnet)
        self.do_getbid_axos(self.session_telnet)
