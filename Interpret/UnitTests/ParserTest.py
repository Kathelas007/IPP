import unittest

from IPPParser import *

doc_write_twice = """<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode20">
    <instruction order="1" opcode="WRITE">
        <arg1 type="string">a</arg1>
        <arg2 type="string">b</arg2>
        <arg3 type="string">c</arg3>
    </instruction>
    <instruction order="2" opcode="WRITE">
        <arg1 type="int">1</arg1>
    </instruction>
</program>"""

doc_bordel = """<?xml version="1.0" encoding="UTF-8"?>
<<aa> <>"""

doc_arg_index1 = """<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode20">
    <instruction order="1" opcode="WRITE">
        <arg1 type="string">Acko</arg1>
        <arg1 type="string">zaseAcko</arg1>
    </instruction>
</program>"""

doc_arg_index2 = """<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode20">
    <instruction order="1" opcode="WRITE">
        <arg2 type="string">a</arg2>
        <arg3 type="string">b</arg3>
    </instruction>
</program>"""

doc_arg_index3 = """<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode20">
    <instruction order="1" opcode="WRITE">
        <arg3 type="string">a</arg3>
    </instruction>
</program>"""


class IterationTestCase(unittest.TestCase):

    def test_instr_iter(self):
        self.parser = IPPParser(doc_write_twice.split('\n'))
        self.parser.parse()
        all_inst = list(self.parser.iter_instructions())

        self.assertListEqual(all_inst, [(1, 'WRITE'), (2, 'WRITE')])

    def test_arg_iter(self):
        self.parser = IPPParser(doc_write_twice.split('\n'))
        self.parser.parse()

        all_args = [[arg for arg in self.parser.iter_arguments()] for _ in self.parser.iter_instructions()]

        self.assertListEqual(all_args, [[('string', 'a'), ('string', 'b'), ('string', 'c')], [('int', '1')]])

    def test_bad_arg(self):
        docs = [doc_arg_index1, doc_arg_index1]

        for doc in docs:
            self.parser = IPPParser(doc.split('\n'))
            self.parser.parse()
            list(self.parser.iter_instructions())
            self.assertRaises(IExc.XMLStructureIE, list, self.parser.iter_arguments())

    def test_well_formatted(self):
        self.parser = IPPParser(doc_bordel.split('\n'))
        self.assertRaises(IExc.XMLFormatIE, self.parser.parse)


if __name__ == '__main__':
    unittest.main()
