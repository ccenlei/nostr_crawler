#!/usr/bin/python3


class RequestUrl(object):
    heads = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}
    cookies = {}
    timeout = 12
    url = ''

    def __init__(self, url=str) -> None:
        self.url = url


class Page(object):
    desc = ''  # list/profit
    cookies = {}
    page_type = ''  # json/html
    page = ''
    src_url = None

    def __init__(self, page=str, src_url=RequestUrl) -> None:
        self.page = page
        self.src_url = src_url

    def cookie_to_str(self):
        c_str = ''
        for n, v in self.cookies.items():
            c_str = c_str + n + "=" + v + "; "
        return c_str


class NostrUser(object):
    pub_key = ''
    name = ''
    dis_name = ''
    desc = ''
    nip05 = ''
    nip05_veri = False
    lud06 = ''
    lud16 = ''
    first_tm = 0
    last_tm = 0
    followed_num = 0
    following_num = 0
    zap_amt = 0
    zap_amt_sent = 0
    twit_veri = False
    twit_handle = ''
    twit_name = ''
    twit_bio = ''
    twit_followers = 0

    def __init__(self, pub_key=str) -> None:
        self.pub_key = pub_key

    def to_json(self):
        return {
            'pub_key': self.pub_key,
            'name': self.name,
            'dis_name': self.dis_name,
            'desc': self.desc,
            'nip05': self.nip05,
            'nip05_veri': self.nip05_veri,
            'lud06': self.lud06,
            'lud16': self.lud16,
            'first_tm': self.first_tm,
            'last_tm': self.last_tm,
            'followed_num': self.followed_num,
            'following_num': self.following_num,
            'zap_amt': self.zap_amt,
            'zap_amt_sent': self.zap_amt_sent,
            'twit_veri': self.twit_veri,
            'twit_handle': self.twit_handle,
            'twit_name': self.twit_name,
            'twit_bio': self.twit_bio,
            'twit_followers': self.twit_followers
        }
