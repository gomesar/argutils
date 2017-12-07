def count_jumps(file_name):
    jumps = []
    with open(file_name, 'r') as input:
        for line in input:
            #print("line {} ".format(line))
            line = line.split('\n')[0]
            jumps.append( int(line) )
    idx = 0
    steps = 0
    while idx >= 0 and idx < len(jumps):

        _idx = idx + jumps[idx]
        jumps[idx] += 1

        steps += 1
        idx = _idx

    print(steps)
    return steps


if __name__ == "__main__":
    count_jumps("jumps")
