import copy
import sys

numbers = [int(x.split('\n')[0]) for x in open(str(sys.argv[1])).read().split('\t')]


size = len(numbers)
states = list()
count = 0
revisited = False
max_val = 0

while revisited == False:
    max_val = max(numbers)
    index = numbers.index(max_val)

    #print("{}. MAX: {}".format(str(numbers), max_val))

    numbers[index] = 0
    for i in range(1, max_val+1):
        _index = (index+i) % size

        #print("{}({}) | ".format(i, _index), end="")
        numbers[_index] += 1

    #print('\n.\t\tCount: {}'.format(count))
    count += 1

    #print(states)
    for s in states:
        if numbers == s:
            #print("{} == {}".format(s, numbers) )
            revisited = True
    states.append(copy.copy(numbers))
print(count)
cycles = states.index(numbers) + 1
resp = count- cycles
print(resp)
