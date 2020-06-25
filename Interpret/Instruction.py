import sys

import abc
import Argument as Arg
import InterpretException as IExc
from IPPMemory import IPPMemory

"""
 Abstract classes
"""


# todo type control

class Instruction(abc.ABC):
    mem = None

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.mem:
            raise IExc.InternIE('Memory must be initialized first')
        self.order = kwargs.pop('order')

    @abc.abstractmethod
    def execute(self):
        pass

    def check_data_types(self, data_types, values):
        if len(data_types) != len(values):
            raise IExc.InterpretException("By check data type both full lists expected")

        result = all(both[0] == type(both[1]) for both in zip(data_types, values))
        if not result:
            raise IExc.OperandTypeIE(f"Can not execute {self} with args {values}")

    def check_same_data_types(self, values):
        result = all(type(values[index]) == type(values[index - 1]) for index in range(0, len(values)))
        if not result:
            raise IExc.OperandTypeIE(f"Can not execute {self} with args {values}")

    def ipp_eq(self, a, b):
        if a is not None and b is not None:
            self.check_same_data_types([a, b])
        return a == b

    @classmethod
    def set_global_memory(cls, memory: IPPMemory):
        cls.mem = memory

    def __cmp__(self, other):
        return (self.order > other.order) - (self.order < other.order)

    def __le__(self, other):
        return self.order <= other.order

    def __lt__(self, other):
        return self.order < other.order

    def __ge__(self, other):
        return self.order >= other.order

    def __gt__(self, other):
        return self.order > other.order

    def __hash__(self):
        return hash(self.order)

    def __repr__(self):
        return f'Order: {self.order}'


class InstructionType:
    @staticmethod
    def check_args(arg_classes: tuple, args: tuple):
        if len(arg_classes) == 0:
            return

        if len(arg_classes) != len(args):
            raise IExc.XMLStructureIE(f'Bad number of operands')

        result = all(isinstance(arg[1], arg[0]) for arg in zip(arg_classes, args))
        if not result:
            raise IExc.XMLStructureIE(f'Bad operand type.')


"""
Types of instruction based on types of arguments
"""


class NoArgI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args(tuple(), prov_args)


class VarI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args((Arg.Var,), prov_args)
        self._var = prov_args[0]


class SymI(InstructionType):
    def __init__(self, *args, **kwargs):
        prov_args = kwargs.pop('prov_args')
        InstructionType.check_args((Arg.Symbol,), prov_args)
        self._sym = prov_args[0]


class LabelI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args((Arg.Label,), prov_args)
        self._label = prov_args[0]


class VarSymSymI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args((Arg.Var, Arg.Symbol, Arg.Symbol), prov_args)
        self._var = prov_args[0]
        self._sym1 = prov_args[1]
        self._sym2 = prov_args[2]


class VarTypeI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args((Arg.Var, Arg.TypeA), prov_args)
        self._var = prov_args[0]
        self._type = prov_args[1]


class VarSymI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args((Arg.Var, Arg.Symbol), prov_args)
        self._var = prov_args[0]
        self._sym = prov_args[1]


class LabelSymSymI(InstructionType):
    def __init__(self, prov_args, *args, **kwargs):
        InstructionType.check_args((Arg.Label, Arg.Symbol, Arg.Symbol), prov_args)
        self._label = prov_args[0]
        self._sym1 = prov_args[1]
        self._sym2 = prov_args[2]


"""
Instruction classes
"""

""" Frames, fnc calls """


class Move(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self._var.value = self._sym.value


class CreateF(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.create_tmp_frame()


class PushF(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.push_tmp_frame()


class PopF(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.pop_tmp_frame()


class DefVar(Instruction, VarI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self._var.define_var()


class Call(Instruction, LabelI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.push_position(self.order)
        return Label.get_label_num(self._label.label)


class Return(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        return self.mem.pop_position()


""" Data stack instructions """


class PushS(Instruction, SymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.push_data_stack(self._sym.value)


class PopS(Instruction, VarI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self._var.value = self.mem.pop_data_stack()


"""Arithmetic, bool,  conversion"""


class Add(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_same_data_types([self._sym1.value, self._sym2.value])
        if type(self._sym1.value) not in [int, float]:
            raise IExc.OperandTypeIE("Can add only int or number")

        self._var.value = self._sym1.value + self._sym2.value


class Sub(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_same_data_types([self._sym1.value, self._sym2.value])
        if type(self._sym1.value) not in [int, float]:
            raise IExc.OperandTypeIE("Can add only int or number")

        self._var.value = self._sym1.value - self._sym2.value


class Mul(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_same_data_types([self._sym1.value, self._sym2.value])
        if type(self._sym1.value) not in [int, float]:
            raise IExc.OperandTypeIE("Can add only int or number")

        self._var.value = self._sym1.value * self._sym2.value


class IDiv(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([int, int], [self._sym1.value, self._sym2.value])

        if self._sym2.value == 0:
            raise IExc.OperandValueIE('Dividing by zero')
        self._var.value = self._sym1.value // self._sym2.value


class Div(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([float, float], [self._sym1.value, self._sym2.value])

        if self._sym2.value == 0:
            raise IExc.OperandValueIE('Dividing by zero')
        self._var.value = self._sym1.value // self._sym2.value


class LT(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        if self._sym1.value is None or self._sym2.value is None:
            raise IExc.OperandTypeIE("Can not compare with nil")

        self.check_same_data_types([self._sym1.value, self._sym2.value])
        self._var.value = self._sym1.value < self._sym2.value


class GT(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        if self._sym1.value is None or self._sym2.value is None:
            raise IExc.OperandTypeIE("Can not compare with nil")

        self.check_same_data_types([self._sym1.value, self._sym2.value])

        self._var.value = self._sym1.value > self._sym2.value


class EQ(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self._var.value = self.ipp_eq(self._sym1.value, self._sym2.value)


class And(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([bool, bool], [self._sym1.value, self._sym2.value])
        self._var.value = self._sym1.value and self._sym2.value


class Or(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([bool, bool], [self._sym1.value, self._sym2.value])
        self._var.value = self._sym1.value or self._sym2.value


class Not(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([bool, ], [self._sym.value, ])
        self._var.value = not self._sym.value.value


class Int2Char(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([int, ], [self._sym.value, ])
        try:
            self._var.value = chr(self._sym.value)
        except ValueError:
            raise IExc.StringIE(f'Can not convert {self._sym.value} to char.')


class Str2Int(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        string = self._sym1.value
        position = self._sym2.value

        self.check_data_types([str, int], [string, position])
        try:
            self._var = ord(string[position])
        except (KeyError, ValueError, IndentationError, IndexError):
            raise IExc.StringIE(f'Can not convert {string} on position {position} to ord value.')


""" Input, output instructions"""


class Read(Instruction, VarTypeI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        line = input()
        self._var.value = self._type.convert_to_type(line)


class Write(Instruction, SymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        try:
            print_value = self._sym.value
        except IExc.NoValueIE:
            print('', end='')
            return

        if print_value is None:
            print('', end='')
        elif type(print_value) == bool:
            if print_value:
                print('true', end='')
            else:
                print('false', end='')
        elif type(print_value) == float:
            print(print_value.hex(), end='')
        else:
            print(print_value, end='')


""" String instructions"""


class Concat(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([str, str], [self._sym1.value, self._sym2.value])
        self._var.value = self._sym1.value + self._sym2.value


class Strlen(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([str, ], [self._sym.value, ])
        self._var.value = len(self._sym.value)


class GetChar(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        string = self._sym1.value
        position = self._sym2.value

        self.check_data_types([str, int], [string, position])

        try:
            self._var.value = string[position]
        except (IndexError, IndentationError):
            raise IExc.StringIE(f'Can not get char from {string} at position {position}')


class SetChar(Instruction, VarSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        variable_string = self._var.value
        position = self._sym1.value
        symb_string = self._sym2.value

        self.check_data_types([str, int, str], [variable_string, position, symb_string])

        char = symb_string[0]

        try:
            variable_string[position] = char
            self._var.value = variable_string
        except (IndentationError, IndexError):
            raise IExc.StringIE(f'Can not get char from {variable_string} at position {position}')


""" Type instructions"""


class Type(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        try:
            value = self._sym.value
        except IExc.NoValueIE:
            self._var.value = ''
            return

        if type(value) == str:
            str_type = 'str'
        elif type(value) == bool:
            str_type = 'bool'
        elif type(value) == int:
            str_type = 'int'
        elif value is None:
            str_type = 'nil'
        elif type(value) == list:
            str_type = ''
        else:
            str_type = ''

        self._var.value = str_type


""" Program flow instructions"""


class Label(Instruction, LabelI):
    _labels = dict()

    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)
        new_label = self._label.label
        if new_label in self._labels:
            raise IExc.SemanticIE(f'Redefinition of label {new_label}')
        self._labels[new_label] = self.order

    def execute(self):
        # no execution !!
        pass

    @classmethod
    def get_label_num(cls, label):
        if label not in cls._labels:
            raise IExc.SemanticIE(f'Label {label} does not exists.')
        else:
            return cls._labels[label]


class Jump(Instruction, LabelI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        return Label.get_label_num(self._label.label)


class JumpIfEq(Instruction, LabelSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        if self.ipp_eq(self._sym1.value, self._sym2.value):
            return Label.get_label_num(self._label.label)


class JumpIfNEq(Instruction, LabelSymSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        if self.ipp_eq(self._sym1.value, self._sym2.value):
            return Label.get_label_num(self._label.label)


class Exit(Instruction, SymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        exit_code = self._sym.value

        self.check_data_types([int, ], [exit_code, ])
        if not (0 <= exit_code <= 49):
            IExc.OperandValueIE('Bad exit code')
        else:
            sys.exit(exit_code)


""" Debug instructions """


class DPrint(Instruction, SymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.debug_print(self._sym.value)


class Break(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.debug_break()


""" Float conversion """


class Int2Float(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([int, ], [self._sym.value])
        self._var.value = float(self._sym.value)


class Float2Int(Instruction, VarSymI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.check_data_types([float, ], [self._sym.value])
        self._var.value = int(self._sym.value)


""" Stack instructions """


class ClearS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        self.mem.clear_data_stack()


class AddS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.check_same_data_types([s1, s2])
        if type(s1) not in [int, float]:
            raise IExc.OperandTypeIE("Can add only int or float")

        self.mem.push_data_stack(s1 + s2)


class SubS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.check_same_data_types([s1, s2])
        if type(s1) not in [int, float]:
            raise IExc.OperandTypeIE("Can sub only int or float")

        self.mem.push_data_stack(s1 - s2)


class MulS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.check_same_data_types([s1, s2])
        if type(s1) not in [int, float]:
            raise IExc.OperandTypeIE("Can mul only int or float")

        self.mem.push_data_stack(s1 * s2)


class IDivS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.check_data_types([int, int], [s1, s2])

        if s2 == 0:
            raise IExc.OperandValueIE('Dividing by zero')

        self.mem.push_data_stack(s1 // s2)


class LTS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        if s1 is None or s2 is None:
            raise IExc.OperandTypeIE("Can not compare with nil")

        self.check_same_data_types([s1, s2])

        self.mem.push_data_stack(s1 < s2)


class GTS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        if s1 is None or s2 is None:
            raise IExc.OperandTypeIE("Can not compare with nil")

        self.check_same_data_types([s1, s2])

        self.mem.push_data_stack(s1 > s2)


class EQS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.mem.push_data_stack(self.ipp_eq(s1, s2))


class AndS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.check_data_types([bool, bool], [s1, s2])
        self.mem.push_data_stack(s1 and s2)


class OrS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        self.check_data_types([bool, bool], [s1, s2])
        self.mem.push_data_stack(s1 or s2)


class NotS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1 = self.mem.pop_data_stack()
        self.check_data_types([bool, ], [s1, ])
        self.mem.push_data_stack(not s1)


class Int2CharS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s = self.mem.pop_data_stack()
        self.check_data_types([int, ], [s, ])
        try:
            self.mem.push_data_stack(chr(s))
        except ValueError:
            raise IExc.StringIE(f'Can not convert {s} to char.')


class Str2IntS(Instruction, NoArgI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        string, position = self.mem.multi_pop_data_stack(2)
        self.check_data_types([str, int], [string, position])
        try:
            self.mem.push_data_stack(ord(string[position]))
        except (KeyError, ValueError, IndentationError, IndexError):
            raise IExc.StringIE(f'Can not convert {string} on position {position} to ord value.')


class JumpIfEqS(Instruction, LabelI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        if self.ipp_eq(s1, s2):
            return Label.get_label_num(self._label.label)


class JumpIfNEqS(Instruction, LabelI):
    def __init__(self, order, args):
        super().__init__(order=order, prov_args=args)

    def execute(self):
        s1, s2 = self.mem.multi_pop_data_stack(2)
        if not self.ipp_eq(s1, s2):
            return Label.get_label_num(self._label.label)


class InstructionBuilder:
    builder_dict = {'MOVE': Move, 'CREATEFRAME': CreateF, 'PUSHFRAME': PushF, 'POPFRAME': PopF, 'DEFVAR': DefVar,
                    'CALL': Call, 'RETURN': Return,
                    'PUSHS': PushS, 'POPS': PopS,
                    'ADD': Add, 'SUB': Sub, 'MUL': Mul, 'IDIV': IDiv, 'DIV': Div,
                    'LT': LT, 'GT': GT, 'EQ': EQ,
                    'AND': And, 'OR': Or, 'NOT': Not,
                    'INT2CHAR': Int2Char, 'STRI2INT': Str2Int,
                    'READ': Read, 'WRITE': Write,
                    'CONCAT': Concat, 'STRLEN': Strlen, 'GETCHAR': GetChar, 'SETCHAR': SetChar,
                    'TYPE': Type,
                    'LABEL': Label,
                    'JUMP': Jump, 'JUMPIFEQ': JumpIfEq, 'JUMPIFNEQ': JumpIfNEq, 'EXIT': Exit,
                    'DPRINT': DPrint, 'BREAK': Break,
                    'INT2FLOAT': Int2Float, 'FLOAT2INT': Float2Int,
                    'CLEARS': ClearS, 'ADDS': AddS, 'SUBS': SubS, 'MULS': MulS, 'IDIVS': IDivS,
                    'LTS': LTS, 'GTS': GTS, 'EQS': EQS, 'ANDS': AndS, 'ORS': OrS, 'NOTS': NotS,
                    'INT2CHARS': Int2CharS, 'STRI2INTS': Str2IntS,
                    'JUMPIFEQS': JumpIfEqS, 'JUMPIFNEQS': JumpIfNEqS}

    def __init__(self, mem=None):
        if mem:
            Instruction.set_global_memory(mem)

    def create_instr(self, order: int, opcode: str, args) -> Instruction:
        opcode = opcode.upper()
        if opcode not in self.builder_dict:
            raise IExc.XMLStructureIE(f'Can not create instruction with opcode {opcode}.')

        instr_class = self.builder_dict[opcode]
        new_instruction = instr_class(order, args)

        return new_instruction
