import unittest

from IPPMemory import *
import InterpretException as IExc


class MemoryTestCase(unittest.TestCase):

    def setUp(self):
        self.mem = IPPMemory()
        self.g_var = [GF, 'a']
        self.l_var = [LF, 'a']
        self.t_var = [TF, 'a']

    def test_set_var(self):
        self.mem.def_var(*self.g_var)
        self.mem.set_var(*self.g_var, 10)
        self.assertEqual(self.mem.get_var(*self.g_var), 10)

    def test_set_non_var(self):
        self.assertRaises(IExc.InterpretException, self.mem.set_var, *self.g_var, 10)

    def test_def_var_twice(self):
        self.mem.def_var(*self.g_var)
        self.assertRaises(IExc.InterpretException, self.mem.def_var, *self.g_var)

    def test_no_LF(self):
        self.assertRaises(IExc.NoFrameIE, self.mem.set_var, *self.l_var, 10)

    def test_no_var(self):
        self.assertRaises(IExc.NoVariableIE, self.mem.get_var, *self.g_var)

    def test_create_tf_twice(self):
        self.mem.create_tmp_frame()
        self.mem.def_var(*self.t_var)
        self.mem.create_tmp_frame()

        self.assertRaises(IExc.NoVariableIE, self.mem.set_var, *self.t_var, 222)

    def test_tf(self):
        self.mem.create_tmp_frame()
        self.mem.def_var(*self.t_var)
        self.mem.set_var(*self.t_var, 20)
        self.assertEqual(self.mem.get_var(*self.t_var), 20)

    def test_tf_twice(self):
        self.mem.create_tmp_frame()
        self.mem.create_tmp_frame()

    def test_push_pop_tf(self):
        self.mem.create_tmp_frame()
        self.mem.def_var(*self.t_var)
        self.mem.set_var(*self.t_var, 20)
        self.mem.push_tmp_frame()

        self.assertEqual(self.mem.get_var(*self.l_var), 20)

        self.mem.set_var(*self.l_var, 42)
        self.mem.pop_tmp_frame()

        self.assertEqual(self.mem.get_var(*self.t_var), 42)

    def test_empty_pop_tf(self):
        self.assertRaises(IExc.NoFrameIE, self.mem.pop_tmp_frame)

    def test_position(self):
        self.mem.push_position(20)
        self.assertEqual(self.mem.pop_position(), 20)

        self.assertRaises(IExc.NoValueIE, self.mem.pop_position)

    def test_data_stack_basic(self):
        self.mem.push_data_stack(2)
        self.mem.push_data_stack(None)

        self.assertEqual(self.mem.pop_data_stack(), None)
        self.assertEqual(self.mem.pop_data_stack(), 2)

    def test_data_stack_empty(self):
        self.mem.push_data_stack(3)
        self.mem.pop_data_stack()

        self.assertRaises(IExc.NoValueIE, self.mem.pop_position)

    def test_dev_test(self):
        self.mem.def_var(*self.g_var)
        self.mem.set_var(*self.g_var, 2)

        self.mem.create_tmp_frame()
        self.mem.def_var(*self.t_var)

        self.mem.push_tmp_frame()
        self.mem.pop_tmp_frame()


class ComplexTests(unittest.TestCase):

    def setUp(self):
        self.mem = IPPMemory()
        self.g_var = [GF, 'a']
        self.l_var = [LF, 'a']
        self.t_var = [TF, 'a']

    def test_second_LF(self):
        mem = IPPMemory()

        mem.create_tmp_frame()
        mem.def_var(*self.t_var)
        mem.set_var(*self.t_var, 5)

        mem.push_tmp_frame()
        self.assertEqual(mem.get_var(*self.l_var), 5)

        mem.create_tmp_frame()
        mem.def_var(*self.t_var)
        mem.set_var(*self.t_var, 10)

        mem.push_tmp_frame()
        self.assertEqual(mem.get_var(*self.l_var), 10)

        mem.pop_tmp_frame()
        self.assertEqual(mem.get_var(*self.l_var), 5)
        self.assertEqual(mem.get_var(*self.t_var), 10)


if __name__ == '__main__':
    unittest.main()
