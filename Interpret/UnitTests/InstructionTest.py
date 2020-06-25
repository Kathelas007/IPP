import unittest
from Instruction import *
from IPPMemory import IPPMemory


class BuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        mem = IPPMemory()
        self.builder = InstructionBuilder(mem)

        self.inst_break = self.builder.create_instr(20, 'BREAK', [])
        self.inst_cf = self.builder.create_instr(40, 'CREATEFRAME', [])

    def test_init_instr(self):
        self.builder.create_instr(2, 'BREAK', [])
        self.assertRaises(IExc.XMLStructureIE, self.builder.create_instr, 10, 'xxx', [])

    def test_exec_instr(self):
        instr = self.builder.create_instr(1, 'CREATEFRAME', [])
        instr.execute()

        instr = self.builder.create_instr(1, 'BREAK', [])
        instr.execute()

        self.inst_break.execute()
        self.inst_cf.execute()


class InstructionTestCase(unittest.TestCase):
    def test_init(self):
        # nelze otestovat kvuli setUp
        # self.assertRaises(IExc.InternIE, CreateF, 2, [])

        mem = IPPMemory()
        Instruction.set_global_memory(mem)

    def setUp(self) -> None:
        mem = IPPMemory()
        self.builder = InstructionBuilder(mem)

        self.i_1 = self.builder.create_instr(1, 'CREATEFRAME', [])
        self.i_2 = self.builder.create_instr(2, 'CREATEFRAME', [])
        self.i_5 = self.builder.create_instr(5, 'CREATEFRAME', [])

    def test_comparing(self):
        self.assertTrue(self.i_1 < self.i_2)
        self.assertTrue(self.i_5 > self.i_2)
        self.assertTrue(self.i_1 <= self.i_2)

    def test_sort(self):
        i_list = [self.i_2, self.i_1, self.i_5, self.i_1]
        i_list.sort()
        sorted_list = [self.i_1, self.i_1, self.i_2, self.i_5]

        self.assertListEqual(i_list, sorted_list)

    def test_hash(self):
        i_a = self.builder.create_instr(1, 'CREATEFRAME', [])
        i_b = self.builder.create_instr(1, 'POPFRAME', [])

        self.assertTrue(i_a, i_b)

    def test_execute(self):
        self.i_1.execute()
        self.i_2.execute()
        self.i_5.execute()


class ParticularInstructionTestCase(unittest.TestCase):
    def setUp(self) -> None:
        mem = IPPMemory()
        self.builder = InstructionBuilder(mem)

    def test_createF(self):
        instr = self.builder.create_instr(1, 'CREATEFRAME', [])
        jump = instr.execute()

        self.assertEqual(jump, None)

class WholePrograms(unittest.TestCase):
    def setUp(self) -> None:
        mem = IPPMemory()
        self.builder = InstructionBuilder(mem)


if __name__ == '__main__':
    unittest.main()
