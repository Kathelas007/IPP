import unittest

from Argument import *
import IPPMemory
from InterpretException import InterpretException as IExc


class BuilderTestCase(unittest.TestCase):
    def setUp(self) -> None:
        memory = IPPMemory.IPPMemory()
        self.builder = ArgumentBuilder(memory)

    def test_basic_inits(self):
        self.builder.create('var', 'LF@a')
        self.builder.create('int', '5')
        self.builder.create('bool', 'false')
        self.builder.create('label', 'label')

        self.assertRaises(IExc, self.builder.create, 'xxx', 'x')


class VarTestCase(unittest.TestCase):
    def setUp(self) -> None:
        memory = IPPMemory.IPPMemory()
        Var.set_global_memory(memory)

        self.var_a = Var('GF@a')

    def test_value_setting(self):
        self.var_a.define_var()
        self.var_a.value = 20
        self.assertEqual(self.var_a.value, 20)


class ConstTestCase(unittest.TestCase):
    def test_const_using(self):
        const = Int('20')
        self.assertEqual(const.value, 20)

        with self.assertRaises(IExc):
            const.value = 2

    def test_bad_init(self):
        self.assertRaises(IExc, Int, True)
        self.assertRaises(IExc, Int, '0oo')

        self.assertRaises(IExc, Bool, 'True')
        self.assertRaises(IExc, Bool, 0)


class LabelCase(unittest.TestCase):
    def test_using(self):
        lab = Label('whatever')
        self.assertEqual(lab.label, 'whatever')
        with self.assertRaises(IExc):
            lab.label = 'other'


class TypeCase(unittest.TestCase):
    def test_using(self):
        tp = TypeA('bool')

        with self.assertRaises(IExc):
            tp.type = 'other'


if __name__ == '__main__':
    unittest.main()
