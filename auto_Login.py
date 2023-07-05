# encoding:UTF-8

from urllib.parse import urlencode
from urllib.request import urlopen
import urllib
import execjs
import time
import socket
def do_encrypt_rc4(src='', passwd ='') :
    i=0
    j = 0
    a = 0
    b = 0
    c = 0

    plen = len(passwd)
    size = len(src)


    key = []

    sbox =[]

    output=[]
    for i in range(0,256):
        key.append( ord(passwd[i % plen]))
        sbox.append(i)
    for i in range(0,256):
        j = (j + sbox[i] + key[i]) % 256
        temp = sbox[i]
        sbox[i] = sbox[j]
        sbox[j] = temp
    for i in range(0,size):

        a = (a + 1) % 256
        b = (b + sbox[a]) % 256
        temp = sbox[a]
        sbox[a] = sbox[b]
        sbox[b] = temp
        c = (sbox[a] + sbox[b]) % 256
        temp = ord(src[i]) ^ sbox[c]
        temp = str(hex(temp))
        print(temp)
        if len(temp) ==  1:
            temp = '0' + temp
        elif len(temp) == 0:
            temp = '00'
        output[i] = temp
    return output.join('')
def test_connect(host,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(5)
    con = False
    try:
        s.connect((host,port))
        con = True
        print('suc_ping')
    except socket.error as e :
        print('fail_ping')
    finally:
        s.close()
    return con
if __name__ == "__main__":
#need to use your username and password 
    username = ""
    password = ""
    jstr ='''
    function do_encrypt_rc4(src, passwd) {
	passwd = passwd + '';
	var i, j = 0, a = 0, b = 0, c = 0, temp;
	var plen = passwd.length,
		size = src.length;

	var key = Array(256); //int
	var sbox = Array(256); //int
	var output = Array(size); //code of data
	for (i = 0; i < 256; i++) {
		key[i] = passwd.charCodeAt(i % plen);
		sbox[i] = i;
	}
	for (i = 0; i < 256; i++) {
		j = (j + sbox[i] + key[i]) % 256;
		temp = sbox[i];
		sbox[i] = sbox[j];
		sbox[j] = temp;
	}
	for (i = 0; i < size; i++) {
		a = (a + 1) % 256;
		b = (b + sbox[a]) % 256;
		temp = sbox[a];
		sbox[a] = sbox[b];
		sbox[b] = temp;
		c = (sbox[a] + sbox[b]) % 256;
		temp = src.charCodeAt(i) ^ sbox[c];//String.fromCharCode(src.charCodeAt(i) ^ sbox[c]);
		temp = temp.toString(16);
		if (temp.length === 1) {
			temp = '0' + temp;
		} else if (temp.length === 0) {
			temp = '00';
		}
		output[i] = temp;
	}
	return output.join('');
}
    '''


    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler(), urllib.request.HTTPHandler(debuglevel=0))
    opener.addheaders = [('User-agent',
                          "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)")]
    url = 'http://2.2.2.3/ac_portal/login.php'
    while True:
        ping = test_connect('www.baidu.com', 80)
        print('ping:',ping)
        if not ping:
            print('net lost ,try connect')
            js = execjs.compile(jstr)
            t = round(time.time() * 1000)
            res = js.call('do_encrypt_rc4', password, t)
            print(t)
            print(res)
            try:
                response = opener.open(url, urlencode(
            {    "opr": "pwdLogin",
                "userName": "13333298122",
            "pwd":str(res),
            "auth_tag": str(t),
            "rememberPwd": "1"}).encode("utf-8"))

                xxx_print = response.read().decode("utf-8")
                isflag = xxx_print.find('true')
                print(xxx_print)
                print(isflag)
                print('```````````````````````````````')
                if  isflag != -1:
                    print('##################################')
                    print('success login')
                    print('##################################')
                else:
                    print('##################################')
                    print('fail login')
                    print('##################################')
            except Exception as e:
                print('```````````````````````````````')
                print('\n\n\n')
                print('##################################')
                print("net error,may need to change url ? ")
                print('##################################')
                print(e)

        if ping:
            print('network ok,now sleep 1200s')
            time.sleep(1200)
