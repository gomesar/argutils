import sys
import socket
import threading

IP          = "0.0.0.0"
PORT        = 0
QUIT_CMD    = "@q"

def ear(s):
    while 1:
        try:
            d, a = s.recvfrom(1024)
            sys.stdout.write("\033[s\033[K\n:"+d+"\033[u")
            sys.stdout.flush()
            #print " {"+d+"} "

            if d.startswith(QUIT_CMD):
                print "[!] DC"
                break;
        except :
            print "[!] Error"
            break
    s.close()

def tongue(s):
    while 1:
        try:
            m = raw_input('>')
            sys.stdout.write("\033[F\033[K")
            sys.stdout.flush()
            if m.startswith(QUIT_CMD):
                s.sendto(m.replace(QUIT_CMD, '@quitting    ') , (IP, PORT))
                print "[!] Quitting"
                break;
            else:
                s.sendto(m, (IP, PORT))
        except:
            break

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))

    ear_h           = threading.Thread(target=ear, args=(s,))
    ear_h.daemon    = True
    ear_h.start()

    tongue(s)
    
    s.close()
