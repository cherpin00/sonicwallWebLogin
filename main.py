import time
import re
from hashlib import md5
import requests
from html.parser import HTMLParser

"""
param1=C31F72D442591AC627E091E49918DEEB
param2=777F1788DDBD2141A6E87925B0ABD4F6
id=ed
sessId=4556063AE86AE70E75CA35F06E5B2B06
select2=English
uName=admin
pass=
digest=530c360c8997065615f1123f6805610e
"""

# Enter your username and password
UNAME = 'admin '
PASSWORD = 'password71'

BEAT_INTERVAL = 15
MIN_RELOGIN = 10

DOMAIN = 'http://webauth.login'
LOGIN_PORTAL = DOMAIN + "/auth1.html"
AUTH_PAGE = DOMAIN + '/auth.cgi'
HEARTBEAT = DOMAIN + '/usrHeartbeat.cgi'
LOGIN_STATUS = DOMAIN + '/loginStatusTop.html'
DYN_LOGIN_STATUS = DOMAIN + '/dynLoginStatus.html?1stLoad=yes'
LOGOUT = DOMAIN + '/dynLoggedOut.html?didLogout=yes'

class InputFieldParser(HTMLParser):
    def handle_starttag(self, tag, attr_pairs):
        if tag != 'input':
            return
        attr_dict = dict(attr_pairs)
        if not 'name' in attr_dict:
            return
        if not 'value' in attr_dict:
            return
        name = attr_dict['name']
        value = attr_dict['value']
        if name == 'sessId':
            print('Session ID,', value)
            self.sess_id = value
        elif name == 'param1':
            print( 'Random param1,', value)
            self.param1 = value
        elif name == 'param2':
            print( 'Random param2,', value)
            self.param2 = value
        elif name == 'id':
            print('ID,',  value)
            self.rid = value

def bake_cookies(p):
    cookies = {}
    cookies['SessId'] = p.sess_id
    page_seed = md5((PASSWORD + p.param2).encode()).hexdigest()
    print('PageSeed, ' + page_seed)
    cookies['PageSeed'] = page_seed
    # Dunno?
    cookies['temp'] = 'temp'
    return cookies

def make_form(p):
    form = {}
    form['param1'] = p.param1
    form['param2'] = p.param2
    form['id'] = p.rid
    form['sessId'] = p.sess_id
    form['select2'] = 'English'
    form['uName'] = UNAME
    form['pass'] = ''
    form['digest'] = md5((p.rid + PASSWORD + p.param1).encode()).hexdigest()
    print("digest is", form['digest'])
    return form

def req_login_page():
    # Disable SSL cert verification
    resp = requests.get(LOGIN_PORTAL, verify = False)
    parser = InputFieldParser()
    parser.feed(resp.text)
    return parser

def parse_beat(data):
    val = re.findall('var remTime=(\d*);', data)[0]
    return int(val)

def do_login():
    # p = req_login_page()
    p = InputFieldParser()
    p.param1="C31F72D442591AC627E091E49918DEEB"
    p.param2="777F1788DDBD2141A6E87925B0ABD4F6"
    p.rid="ed"
    p.sess_id="4556063AE86AE70E75CA35F06E5B2B06"
    # p.select2="English"
    # p.uName="admin"
    # p.pass=""
    # p.digest="530c360c8997065615f1123f6805610e"
    print('Got login page')
    cookies = bake_cookies(p)
    form = make_form(p)
    print(form)
    return
    login_req = requests.post(AUTH_PAGE, data = form, cookies = cookies, verify = False)
    if login_req.status_code != 200:
        raise Exception('Error in logging in')
    # TODO: How do we handle the redirect
    if login_req.text.find('auth.html') != -1:
        raise Exception('Invalid credentials/Already logged in')
    print('Logged in successfully')
    requests.get(LOGIN_STATUS, cookies = cookies, verify = False)
    requests.get(DYN_LOGIN_STATUS, cookies = cookies, verify = False)
    return cookies

def main():
    cookies = do_login()
    return
    try:
        while True:
            beat_req = requests.post(HEARTBEAT, cookies = cookies, verify = False)
            rem_time = parse_beat(beat_req.text)
            print('Heatbeat ..*..', rem_time)
            if rem_time < MIN_RELOGIN:
                print('Re-logging in...')
                cookies = do_login()
            time.sleep(BEAT_INTERVAL)
    finally:
        print('Exit. Logging out...')
        requests.get(LOGOUT, verify = False)


if __name__ == '__main__':
    main()