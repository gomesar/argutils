import sys
import socket
import threading
# Crypt
import md5
import base64
from Crypto.Cipher import AES
from Crypto import Random

IP          = "0.0.0.0"
PORT        = 0
QUIT_CMD    = "@q"
KEY         = "1t5n0tS4f3"
# Crypt
BS      = 16 # Block size
pad     = lambda s : s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad   = lambda s : s[:-ord(s[len(s)-1:])]
trans   = lambda k : md5.new(k).digest()

def printErro(err):
    print type(err)
    print err.args
    print err

def enc(raw, key):
    try:
        iv      = Random.new().read(AES.block_size)
        key_md5 = trans(key)
        cipher  = AES.new(key_md5, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(pad(raw)) )
    except Exception as err:
        printErro(err)

def dec(cph, key):
    try:
        cph_d   = base64.b64decode(cph)
        iv      = cph_d[:BS]
        key_md5 = trans(key)
        cipher  = AES.new(key_md5, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(cph_d[BS:]) )
    except Exception as err:
        printErro(err)

def ear(s):
    while 1:
        try:
            d, a = s.recvfrom(1024)
            d = dec(d, KEY)

            sys.stdout.write("\033[s\n\033[K:"+d+"\033[u")
            sys.stdout.flush()
            #print " {"+d+"} "

            if d.startswith(QUIT_CMD):
                print "[!] DC"
                break;
        except Except as err:
            print "[!] Error E"
            printErro(err)
            break
    s.close()

def tongue(s):
    while 1:
        try:
            m = raw_input('>')
            sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()
            if m.startswith(QUIT_CMD):
                m = m.replace(QUIT_CMD, '@quitting    ')
                s.sendto(enc(m, KEY), (IP, PORT))
                print "[!] Quitting"
                s.close()
                break;
            else:
                s.sendto(enc(m, KEY), (IP, PORT))
        except Exception as err:
            #print "[!] Error T"
            #printErro(err)
            break

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))

    ear_h           = threading.Thread(target=ear, args=(s,))
    ear_h.daemon    = True
    ear_h.start()

    tongue(s)

