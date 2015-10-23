import re


class Operand(object):
    def read(self, processor):
        pass

    def write(self, processor, value):
        pass

    @staticmethod
    def parse_operand(op_str, exepect_label=False):
        op_str = op_str.strip()
        if exepect_label and re.match("[a-z]\w*", op_str, re.IGNORECASE) is not None:
            return Label(op_str)
        if op_str[0] == '#':  # constant
            return Constant(int(op_str[1::], 16))
        elif op_str[0] == '(':
            return Pointer(int(op_str[1:-1], 16) - 1)
        else:
            return Address(int(op_str, 16) - 1)


class Label(Operand):

    def __init__(self, label):
        super(Label, self).__init__()
        self._label = label

    # Return the string label
    def read(self, processor):
        return self._label

    def write(self, processor, value):
        raise NotImplementedError()

    def __repr__(self):
        return "'{}'".format(self._label)


class Address(Operand):

    def __init__(self, addr):
        super(Address, self).__init__()
        self._addr = addr  # id of the memory array

    def read(self, processor):
        return processor.memory()[self._addr]

    def write(self, processor, value):
        processor.memory()[self._addr] = value

    def __repr__(self):
        return "{}".format(self._addr)


class Pointer(Operand):

    def __init__(self, ptr):
        super(Pointer, self).__init__()
        self._ptr = ptr

    def read(self, processor):
        return processor.memory()[self._get_addr(processor)]

    def write(self, processor, value):
        processor.memory()[self._get_addr(processor)] = value

    def _get_addr(self, processor):
        return processor.memory()[self._ptr]

    def __repr__(self):
        return "({})".format(self._ptr)


class Constant(Operand):

    def __init__(self, cste):
        super(Constant, self).__init__()
        self._cste = cste

    # Return the string label
    def read(self, processor):
        return self._cste

    def write(self, processor, value):
        raise NotImplementedError()

    def __repr__(self):
        return "#{}".format(self._cste)


class Instruction(object):

    #
    # OPCODES
    #
    PRINT = 0
    MOVE = 1
    ADD = 2
    SUB = 3
    AND = 4
    OR = 5
    XOR = 6
    COMP = 7
    BEQ = 8
    BNE = 9
    BGT = 10
    BLT = 11
    BGE = 12
    BLE = 13

    COMP_LT = 14
    COMP_GT = 15
    COMP_LE = 16
    COMP_GE = 17
    COMP_EQ = 18
    COMP_NEQ = 19

    def __init__(self, opcode, op1, op2=None):
        self._opcode = opcode
        self._op1 = op1
        self._op2 = op2

    # execute the address of the next instruction to execute
    def exec(self, processor):
        if self._opcode == Instruction.MOVE:
            self._op2.write(processor, self._op1.read(processor))
        elif self._opcode == Instruction.ADD or self._opcode == Instruction.AND or self._opcode == Instruction.OR \
                or self._opcode == Instruction.SUB or self._opcode == Instruction.XOR:
            a = self._op2.read(processor)
            b = self._op1.read(processor)
            self._op2.write(processor, self._get_opcode_func()(a, b))
        elif self._opcode == Instruction.COMP or self._opcode == Instruction.COMP_EQ \
              or self._opcode == Instruction.COMP_GE or self._opcode == Instruction.COMP_GT \
                or self._opcode == Instruction.COMP_LE or self._opcode == Instruction.COMP_NEQ:
            a = self._op2.read(processor)
            b = self._op1.read(processor)
            processor.set_comp(self._get_opcode_func()(a, b))
        elif self._opcode == Instruction.PRINT:
            start = self._op1._addr
            end = (self._op2._addr if self._op2 else start) + 1
            print(' '.join(processor.memory()[start:end]))
        else:  # branch
            if processor.comp():
                return processor.label2pc(self._op1.read())
        return processor.pc() + 1

    def _get_opcode_func(self):
        import operator
        if self._opcode == Instruction.ADD:
            return operator.add
        elif self._opcode == Instruction.SUB:
            return operator.sub
        elif self._opcode == Instruction.AND:
            return operator.and_
        elif self._opcode == Instruction.OR:
            return operator.or_
        elif self._opcode == Instruction.XOR:
            return operator.xor
        elif self._opcode == Instruction.COMP or self._opcode == Instruction.COMP_LT: # by default less than
            return operator.lt
        elif self._opcode == Instruction.COMP_EQ:
            return operator.eq
        elif self._opcode == Instruction.COMP_GE:
            return operator.ge
        elif self._opcode == Instruction.COMP_GT:
            return operator.gt
        elif self._opcode == Instruction.COMP_LE:
            return operator.le
        elif self._opcode == Instruction.COMP_NEQ:
            return operator.ne
        else:
            raise RuntimeError("No function")

    def __repr__(self):
        return "{} {},{}".format(self._opcode, self._op1, self._op2)

    def opcode(self):
        return self._opcode

    def specify_comp(self, branch_op):
        if self._opcode != Instruction.COMP:
            return
        if branch_op == Instruction.BNE:
            self._opcode = Instruction.COMP_NEQ
        elif branch_op == Instruction.BLT:
            self._opcode = Instruction.COMP_LT
        elif branch_op == Instruction.BLE:
            self._opcode = Instruction.COMP_LE
        elif branch_op == Instruction.BGT:
            self._opcode = Instruction.COMP_GT
        elif branch_op == Instruction.BEQ:
            self._opcode = Instruction.COMP_EQ
        elif branch_op == Instruction.BGE:
            self._opcode = Instruction.COMP_GE

    @staticmethod
    def parse(str_instruction):
        components = re.split("\s+", str_instruction)

        # read label if there is one
        label = None
        if len(components) == 3:
            label = components[0]
            components = components[1::]

        # read op
        opcode = Instruction._str2opcode(components[0].strip())
        op1, op2 = Instruction._parse_operands(opcode, components[1])
        return Instruction(opcode, op1, op2), label

    @staticmethod
    def _parse_operands(opcode, operands_raw):
        operands = operands_raw.split(",")

        op1 = Operand.parse_operand(operands[0], Instruction.is_branch(opcode))
        op2 = None
        if len(operands) > 1:
            op2 = Operand.parse_operand(operands[1])

        return op1, op2

    @staticmethod
    def is_branch(opcode):
        return opcode == Instruction.BEQ or opcode == Instruction.BGE or opcode == Instruction.BGT \
                or opcode == Instruction.BLE or opcode == Instruction.BLT or opcode == Instruction.BNE

    @staticmethod
    def _str2opcode(str_op):
        if str_op == "PRINT":
            return Instruction.PRINT
        elif str_op == "MOVE":
            return Instruction.MOVE
        elif str_op == "ADD":
            return Instruction.ADD
        elif str_op == "SUB":
            return Instruction.SUB
        elif str_op == "AND":
            return Instruction.AND
        elif str_op == "OR":
            return Instruction.OR
        elif str_op == "XOR":
            return Instruction.XOR
        elif str_op == "COMP":
            return Instruction.COMP
        elif str_op == "BEQ":
            return Instruction.BEQ
        elif str_op == "BNE":
            return Instruction.BNE
        elif str_op == "BGT":
            return Instruction.BGT
        elif str_op == "BLT":
            return Instruction.BLT
        elif str_op == "BGE":
            return Instruction.BGE
        elif str_op == "BLE":
            return Instruction.BLE
        else:
            raise RuntimeError("Unknown instruction '{}'".format(str_op))


class Processor(object):

    def __init__(self, memory, labels, code):
        self._comp = 0
        self._pc = 0
        self._memory = memory
        self._labels = labels
        self._code = code

    def tick(self):
        if self._pc >= len(self._code):
            raise IndexError()
        self._pc = self._code[self._pc].exec(self)

    def pc(self):
        return self._pc

    def memory(self):
        return self._memory

    def comp(self):
        return self._comp

    def set_comp(self, comp):
        self._comp = comp

    def label2pc(self, label):
        return self._labels[label]


class AssemblySimulator(object):

    def __init__(self, code, labels, memory_size=0xFF):
        self.processor = Processor([0] * memory_size, labels, code)

    def run(self):
        try:
            while True:
                self.processor.tick()
        except IndexError:
            pass

    @staticmethod
    def parse():
        code = []
        labels = {}
        memory_size = 0
        try:
            memory_size = int(input(), 16)
            curr_addr = 0
            row = input()
            while row != "":
                instr, label = Instruction.parse(row)

                if label is not None:
                    labels[label] = curr_addr

                if Instruction.is_branch(instr.opcode()) and curr_addr > 0:
                    code[curr_addr - 1].specify_comp(instr.opcode())

                code.append(instr)
                curr_addr += 1
                row = input()
        except IOError:
            pass
        return AssemblySimulator(code, labels, memory_size=memory_size)

if __name__ == "__main__":
    sim = AssemblySimulator.parse()
    sim.run()
