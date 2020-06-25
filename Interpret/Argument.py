import re
import InterpretException as IExc
import abc


def catch_init_error(cls_name, errors):
    """ Catches exception when its not possible to create new argument"""

    def func_decorator(func):
        def func_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors:
                raise IExc.XMLStructureIE(f'Can not initialize {cls_name} with values arg: {args[1:]}, kwarg: {kwargs}')

        return func_wrapper

    return func_decorator


class Symbol(abc.ABC):
    @property
    def value(self):
        return self.value

    @value.setter
    @abc.abstractmethod
    def value(self, value):
        pass

    def __repr__(self):
        return f'{self.__class__}, Value: {self.value}'


class Var(Symbol):
    memory = None
    frame_dict = {'GF': 0, 'LF': 1, 'TF': 2}
    delimiter = '@'

    @catch_init_error('Var', (KeyError, IndexError))
    def __init__(self, frame_name: str):
        if not self.memory:
            raise IExc.InternIE('Can not init variable without memory')

        if self.delimiter not in frame_name:
            raise IExc.InternIE(f'Bad variable format, missing {self.delimiter}.')

        frame, self._name = frame_name.split(self.delimiter, 2)

        if frame not in self.frame_dict:
            raise IExc.InternIE(f'Bad frame format of {frame_name}')

        self._frame = self.frame_dict[frame]

    @property
    def value(self):
        return self.memory.get_var(self._frame, self._name)

    @value.setter
    def value(self, value):
        self.memory.set_var(self._frame, self._name, value)

    @property
    def id(self):
        return self._frame, self._name

    def define_var(self):
        self.memory.def_var(*self.id)

    @classmethod
    def set_global_memory(cls, memory):
        cls.memory = memory

    @classmethod
    def set_frame_dict(cls, dictionary: dict):
        cls.frame_dict = dictionary

    @classmethod
    def set_delimiter(cls, delimiter: str):
        cls.delimiter = delimiter


class Constant(Symbol, abc.ABC):
    _value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        raise IExc.OperandTypeIE('Can not change constant value.')


class Int(Constant):
    @catch_init_error('Int', ValueError)
    def __init__(self, value: str):
        if type(value) != str:
            raise IExc.InternIE('Init value of Int must be string')
        self._value = int(value)


class Bool(Constant):
    bool_dict = {'true': True, 'false': False}

    @catch_init_error('Bool', KeyError)
    def __init__(self, value):
        if type(value) == bool:
            self._value = value
        else:
            self._value = self.bool_dict[value]


class String(Constant):
    def __init__(self, value: str):
        value = self._replace_ascii(value)
        self._value = value

    def _replace_ascii(self, value):
        indexes = [f.start() for f in re.finditer("""(?<=\\\)[\d]{3}""", value)]
        indexes.reverse()

        for index in indexes:
            new_char = chr(int(value[index:index + 3]))
            value = value[:index - 1] + new_char + value[index + 3:]

        return value


class Nil(Constant):
    def __init__(self, *ignor, **double_ignor):
        self._value = None


class Label:
    def __init__(self, value):
        self._label = value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        raise IExc.OperandTypeIE('Can not change label value.')

    def __repr__(self):
        return f'{self.__class__}, Value: {self.label}'


class FloatA(Constant):
    @catch_init_error('Float', ValueError)
    def __init__(self, value: str):
        if type(value) != str:
            raise IExc.InternIE('Init value of Float must be string')
        self._value = float.fromhex(value)


class TypeA:
    type_dict = {'int': Int, 'bool': Bool, 'string': String, 'float': FloatA}

    @catch_init_error('TypeI', KeyError)
    def __init__(self, value):
        self._type = self.type_dict[value]

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        raise IExc.OperandTypeIE('Can not change type value.')

    def convert_to_type(self, conv: str):
        conv_lower = conv.lower

        if conv_lower == 'true' or conv_lower == 'false':
            conv = conv_lower

        try:
            argument = self.type(conv)
            return argument.value

        except IExc:
            return None

    def __repr__(self):
        return f'{self.__class__}, Value: {self.type.__class__}'


class ArgumentBuilder:
    builders = {'int': Int, 'bool': Bool, 'string': String, 'nil': Nil,
                'label': Label, 'type': TypeA, 'var': Var, 'float': FloatA}

    def __init__(self, memory=None):
        if memory:
            Var.set_global_memory(memory)

    @catch_init_error('Argument', (TypeError, KeyError))
    def create(self, a_type: str, value: str):
        if a_type not in self.builders:
            raise IExc.XMLStructureIE('Bad argument type.')
        return self.builders[a_type](value)
