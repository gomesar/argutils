'''
	Alternative way:
	sum([max(l) - min(l) for l in [ [int(i.split('\n')[0]) for i in w.split('\t')] for w in tuple(open("checksum.csv"))]])
'''
def do_cksum(file_name):
    li = list()
    sum = 0

    with open(file_name, "r") as csv:
        for line in csv:
            line = line.replace("\n","").split("\t")
            line = [int(x) for x in line]

            #print(line)
            mi = int(min(line))
            ma = int(max(line))
            tt = ma - mi
            #print( "Max - Min = {} - {} = {}".format(ma, mi, tt) )
            sum += tt
        print(sum)


if __name__ == "__main__":
    file_name = "checksum.csv"
    do_cksum(file_name)
