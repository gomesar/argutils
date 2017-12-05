def do_cksum(file_name, verbose=False):
    li = list()
    sum = 0

    with open(file_name, "r") as csv:
        aux = 0
        for line in csv:
            line = line.replace("\n","").split("\t")
            line = [int(x) for x in line]
            for i in range(len(line)):
                for j in range(i+1, len(line)):
                    if line[i] % line[j] == 0:
                        if verbose: print("{} / {} == 0".format(line[i], line[j]) )
                        sum += line[i] /line[j]
                    elif line[j] % line[i] == 0:
                        if verbose: print("{} / {} == 0".format(line[j], line[i]) )
                        sum += line[j] /line[i]


            #print(line)
        print(sum)


if __name__ == "__main__":
    #test = "test.csv"
    #do_cksum(test)

    file_name = "checksum.csv"
    do_cksum(file_name)
