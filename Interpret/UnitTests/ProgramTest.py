import unittest.mock

from IPPMemory import IPPMemory
from Program import *


class FakeInstruction:
    called_order = []

    def __init__(self, order, jump):
        self.order = order
        self.jump = jump

    def execute(self):
        self.called_order.append(self.order)
        return self.jump

    @classmethod
    def clean_counter(cls):
        cls.called_order = []

    def __hash__(self):
        return hash(self.order)

    def __lt__(self, other):
        return self.order < other.order

    def __repr__(self):
        return f'Order: {self.order}, Jump: {self.jump}'


class InitTestCase(unittest.TestCase):
    def setUp(self) -> None:
        mem = IPPMemory()
        self.program = Program(mem)

    def test_basic_init(self):
        self.program.start_instruction_init()
        self.program.add_instruction(3)
        self.program.add_instruction(5)
        self.program.add_instruction(2)
        self.program.end_instruction_init()

        self.assertListEqual(self.program.instructions, [2, 3, 5])

    def test_not_uniq(self):
        self.program.start_instruction_init()
        self.program.add_instruction(3)
        self.program.add_instruction(3)

        self.assertRaises(IExc.XMLStructureIE, self.program.end_instruction_init)


class ExecuteTestCase(unittest.TestCase):
    def setUp(self) -> None:
        mem = IPPMemory()
        self.program = Program(mem)
        self.program.start_instruction_init()

        self.i_0 = FakeInstruction(0, None)
        self.i_6 = FakeInstruction(6, None)
        self.i_1 = FakeInstruction(1, self.i_6)  # doufam, ze totok bude fungovat u Instructions
        self.i_5 = FakeInstruction(5, None)

    def test_jumps(self):
        FakeInstruction.clean_counter()
        # (0, None), (1, 6), (5, None), (6, None)
        self.program.add_instruction(self.i_0)
        self.program.add_instruction(self.i_1)
        self.program.add_instruction(self.i_5)
        self.program.add_instruction(self.i_6)

        self.program.end_instruction_init()

        self.program.execute_program()

        self.assertListEqual(FakeInstruction.called_order, [0, 1, 6])

    def test_bad_jumps(self):
        self.program.add_instruction(self.i_0)
        self.program.add_instruction(self.i_1)
        self.program.add_instruction(self.i_5)
        self.program.end_instruction_init()

        self.assertRaises(IExc.SemanticIE, self.program.execute_program)


if __name__ == '__main__':
    unittest.main()
