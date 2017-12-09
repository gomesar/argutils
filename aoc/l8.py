import sys


class Instruction:
    def __init__(self, line):
        _values = line.split(' ')
        # b inc 5 if a > 1
        self.reg = _values[0]       # b
        self.opr = _values[1]       # inc
        self.val = int(_values[2])  # 5
        #
        self.rop = _values[4]       # a
        self.tes = _values[5]       # >
        self.rva = int(_values[6])  # 1

    def __str__(self):
        return "{} {} {} if {} {} {}".format(self.reg, self.opr, self.val, self.rop, self.tes, self.rva)


class Processor:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.instructions = list()
        self.registers = dict()
        self.largest_ever = {
            "reg": None,
            "val": -1
        }
        self.largest = {
            "reg": None,
            "val": -1
        }


    def verify_ins(rop_val, tes, rva):
        if tes == "<":
            return True if rop_val < rva else False
        if tes == "<=":
            return True if rop_val <= rva else False
        if tes == "==":
            return True if rop_val == rva else False
        if tes == ">=":
            return True if rop_val >= rva else False
        if tes == ">":
            return True if rop_val > rva else False
        if tes == "!=":
            return True if rop_val != rva else False
        print("[!] Unknow 'tes'")
        raise Exception


    def read_instructions(self, file_name):
        self.instructions = list()
        for l in tuple(open(file_name)):
            self.instructions.append( Instruction(l.split('\n')[0]) )


    def calc(self):
        for ins in self.instructions:
            if ins.rop not in self.registers:
                self.registers[ins.rop] = 0
            if ins.reg not in self.registers:
                self.registers[ins.reg] = 0

            if Processor.verify_ins(self.registers[ins.rop], ins.tes, ins.rva):
                if ins.opr == "inc":
                    if self.verbose:
                        print("{}\n\t".format(str(ins)), end="")
                        print("{}: {}".format(ins.reg, self.registers[ins.reg]), end="")
                    self.registers[ins.reg] += ins.val
                    if self.verbose:  print(" => {}".format(self.registers[ins.reg]))
                elif ins.opr == "dec":
                    if self.verbose:
                        print("{}\n\t".format(str(ins)), end="")
                        print("{}: {}".format(ins.reg, self.registers[ins.reg]), end="")
                    self.registers[ins.reg] -= ins.val
                    if self.verbose: print(" => {}".format(self.registers[ins.reg]))

                if self.registers[ins.reg] >= self.largest_ever['val']:
                    self.largest_ever['val'] = self.registers[ins.reg]
                    self.largest_ever['reg'] = ins.reg

        for r, v in self.registers.items():
            if v >= self.largest["val"]:
                self.largest = {"reg": r, "val": v}
        print("Largest:      r:{}, v:{}.".format(self.largest["reg"], self.largest["val"]))
        print("Largest ever: r:{}, v:{}.".format(self.largest_ever["reg"], self.largest_ever["val"]))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use: python3 l8.py file_name")
    else:
        processor = Processor()
        processor.read_instructions(sys.argv[1])
