import sys

class day10:
    def __init__(self):
        self.n = list(range(256))
        self.size = len(self.n)


    def revert(self, c, l):
        if c + l >= self.size:
            tmp = list(self.n)
            for i in range(c+l - self.size + 1):
                tmp.append(tmp[i])
            _rev = tmp[c : c+l]
            _rev = _rev[::-1]
            #print("[+] Reversing: {}".format(str(_rev)))
            tmp[c:c+l] = _rev

            for idx in range(c, c+l):
                self.n[ (idx) % self.size ] = tmp[idx]
        else:
            _rev = self.n[c:c+l]
            _rev =_rev[::-1]
            #print("[-] Reversing: {}".format(str(_rev)))
            self.n[c:c+l] = _rev

    def do(self, file_name, rounds):
        lenghts = [ int(x) for x in open(file_name).read().split('\n')[0].split(',') ]
        #lenghts = [ ord(x) for x in open(file_name).read().split('\n')[0] ]
        #lenghts.extend([7, 31, 73, 47, 23])
        #print("Lenghts: {}".format(str(lenghts)))

        curr = 0
        skip = 0

        for _r in range(int(rounds)):
            for l in lenghts:
                #print("curr:{}. skip: {}. lenght: {}\n\t{}".format(curr, skip, l, str(self.n)))
                self.revert(curr, int(l))
                curr += l + skip

                skip += 1
        print("[FINAL] curr:{}. skip: {}. lenght: {}\n\t{}".format(curr, skip, l, str(self.n)))
        print("Result: {}".format(self.n[0] * self.n[1]))
        #digest = self.digest()
        #hex_digest = ''.join(['{:02x}'.format(x) for x in digest])
        #print("Digest: {}".format( hex_digest) )


    def digest(self):
        digest = list()
        for block in range(16):
            offset = block * 16
            bvalue = self.n[offset]
            for b in range(1,16):# 1~15 => 2-16
                idx = offset + b
                bvalue ^= self.n[idx]
            digest.append(bvalue)
        return digest

if __name__ == "__main__":
    d10 = day10()
    d10.do(sys.argv[1], sys.argv[2])
