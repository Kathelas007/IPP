import InterpretException as IExc

frame_dict = {'GF': 0, 'LF': 1, 'TF': 2}
GF = 0
LF = 1
TF = 2


class FrameList(list):
    def __getitem__(self, item):

        try:
            return_item = super().__getitem__(item)
        except KeyError:
            raise IExc.NoFrameIE(f'There is no frame {item}')

        if return_item is None:
            raise IExc.NoFrameIE(f'There is no frame {item}')

        return return_item


class IPPMemory:

    def __init__(self):
        self._frames = FrameList([dict(), None, None])
        self._frame_stack = list()
        self._position_stack = list()
        self._data_stack = list()

    def __repr__(self):
        return f'Frames: {self._frames}'

    def def_var(self, frame, var_key):
        if var_key in self._frames[frame]:
            raise IExc.SemanticIE(f'Variable {var_key} already defined.')
        self._frames[frame][var_key] = []

    def set_var(self, frame, var_key, value):
        if var_key not in self._frames[frame]:
            raise IExc.NoVariableIE(f'Variable {var_key} not defined.')
        self._frames[frame][var_key] = value

    def get_var(self, frame, var_key):
        if var_key not in self._frames[frame]:
            raise IExc.NoVariableIE(f'Variable {var_key} not defined.')
        ret_val = self._frames[frame][var_key]
        if type(ret_val) == list:
            raise IExc.NoValueIE(f'Variable {var_key} has no value.')

        return ret_val

    def create_tmp_frame(self):
        self._frames[TF] = dict()

    def push_tmp_frame(self):
        if not self._frames[2]:
            raise IExc.NoFrameIE('No tmp frame to push stack. ')
        # loc = tmp
        self._frames[1] = self._frames[2]
        # tmp not initiated
        self._frames[2] = None
        # local to stack
        self._frame_stack.append(self._frames[1])

    def pop_tmp_frame(self):
        if len(self._frame_stack) == 0:
            raise IExc.NoFrameIE(f'No frame on stack.')

        # remove last one
        last_on_stack = self._frame_stack.pop(-1)
        # loc to tmp
        self._frames[2] = last_on_stack
        # set loc
        try:
            self._frames[1] = self._frame_stack[0]
        except IndexError:
            self._frames[1] = None

    def push_position(self, position: int):
        self._position_stack.append(position)

    def pop_position(self):
        if len(self._position_stack) == 0:
            raise IExc.NoValueIE('Can not pop position.')
        return self._position_stack.pop(-1)

    def push_data_stack(self, data):
        self._data_stack.append(data)

    def pop_data_stack(self):
        if len(self._data_stack) == 0:
            raise IExc.NoValueIE('No values on data stack')
        return self._data_stack.pop(-1)

    def multi_pop_data_stack(self, num):
        result = [self.pop_data_stack() for _ in range(0, num)]
        result.reverse()
        return result

    def clear_data_stack(self):
        self._data_stack = []

    def debug_print(self, value):
        print(value)

    def debug_break(self):
        print(self._frames)
