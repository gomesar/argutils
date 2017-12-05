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


    def do_spiral(self, number):
        for i in range(1, number):
            self.step()

        if self.verbose: print("x: {}, y: {}".format(self.x, self.y))
        print(abs(self.x) + abs(self.y))


if __name__ == "__main__":

    if len(sys.argv) == 2:
        s = Spiral()
        s.do_spiral(int(sys.argv[1]))
