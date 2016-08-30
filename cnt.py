import socket
import threading

IP      = "0.0.0.0"
PORT    = 0

def ear(s):
    while 1:
        try:
            d, a = s.recvfrom(1024)
            print ">{", d, "}"
        except :
            print "[!] Error"
            break


def tongue(s):
    while 1:
        try:
            m = raw_input(':')
            if m.startswith('@quit'):
                s.sendto(m.replace('@quit', '@Quitting!    ') , (IP, PORT))
                print "[!] Quitting"
                break;
            else:
                s.sendto(m, (IP, PORT))
        except:
            break
    s.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', PORT))

    ear_h       = threading.Thread(target=ear, args=(s,))
    ear_h.daemon = True
    ear_h.start()

    tongue(s)
    
