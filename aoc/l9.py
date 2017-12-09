import sys


class Line:
    def __init__(self, line):
        self.score, self.garbage = Line.__parse(line)


    def __parse(line):
        score = 0
        gcount = 0

        opens = 0
        _scape = False
        _garbage = False
        for c in range(len(line)):
            if _scape:
                _scape = False
            elif _garbage:
                if line[c] == '!':
                    _scape = True
                elif line[c] == ">":
                    _garbage = False
                else:
                    gcount += 1
            else:
                if line[c] == '!':
                    _scape = True
                elif line[c] == '<':
                    _garbage = True
                elif line[c] == "{":
                    opens += 1
                elif line[c] == "}":
                    score += opens
                    opens -= 1
        print("Score: {}. Garbage: {}".format(score, gcount))
        return score, gcount


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python3 l9.py file_name")
    else:
        for line in tuple(open(sys.argv[1])):
            if len(line) <= 40:
                print("Test: {}".format(line))
            Line(line.split('\n')[0])
