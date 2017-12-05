import sys


class Spiral():


    def __init__(self, verbose=False):
        self.verbose = verbose
        self.x = 0
        self.y = 0
        self.d = 0
        self.num_steps = 1
        self.side = 0
        self.two_corners = 0
        self.directions = ['r', 'u', 'l', 'b']
        self.dict = {"00": 1}


    def cal_value(self):
        key = "{}{}".format(self.x, self.y)
        value = 0

        for i in range(8):
            if i == 0:
                _x = self.x + 1
                _y = self.y
            elif i == 1:
                _x = self.x + 1
                _y = self.y + 1
            elif i == 2:
                _x = self.x
                _y = self.y + 1
            elif i == 3:
                _x = self.x - 1
                _y = self.y + 1
            elif i == 4:
                _x = self.x - 1
                _y = self.y
            elif i == 5:
                _x = self.x - 1
                _y = self.y - 1
            elif i == 6:
                _x = self.x
                _y = self.y - 1
            elif i == 7:
                _x = self.x + 1
                _y = self.y - 1

            _key = "{}{}".format(_x, _y)
            if _key in self.dict:
                value += self.dict[_key]

        self.dict[key] = value
        return value


    def step(self):
        d = self.d
        #print("Step to: {}".format(self.directions[d]))

        if self.directions[d] == 'r':
            self.x+= 1
        elif self.directions[d] == 'u':
            self.y += 1
        elif self.directions[d] == 'l':
            self.x -= 1
        elif self.directions[d] == 'b':
            self.y -= 1
        self.side += 1

        if self.side % self.num_steps == 0:
            self.d = (self.d + 1 ) % 4
            self.side = 0

            self.two_corners += 1
            if self.two_corners % 2 == 0:
                self.num_steps += 1

        return self.cal_value()


    def do_spiral(self, number):
        value = 0
        for i in range(1, number):
            value = self.step()
            if value > number:
                break

        print(value)


if __name__ == "__main__":

    if len(sys.argv) == 2:
        s = Spiral()
        s.do_spiral(int(sys.argv[1]))
