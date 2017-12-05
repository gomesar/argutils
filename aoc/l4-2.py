

def check_anagram(word1, word2):
    return sorted(word1) == sorted(word2)


def check_passwords(file_name):
    with open(file_name, 'r') as input:
        sum = 0

        for line in input:
            words = line.split()
            _ok = True

            for i in range( len(words) ):
                for j in range(i+1, len(words) ):
                    if check_anagram(words[i], words[j]):
                        _ok = False
                        print("Anagram: {} == {}".format(words[i], words[j]))
            if _ok:
                sum += 1
    print(sum)
    return sum


if __name__ == "__main__":
    check_passwords("input")
