import InterpretException as IExc
from Instruction import Return
from IPPMemory import IPPMemory


class Program:
    def __init__(self, mem):
        self.mem = mem
        self.instructions = []

    def start_instruction_init(self):
        self.instructions = []

    def add_instruction(self, instruction):
        self.instructions.append(instruction)

    def end_instruction_init(self):
        # check uniq
        if len(self.instructions) != len(set(self.instructions)):
            raise IExc.XMLStructureIE('Instructions do not have uniq order')
        # sort
        self.instructions.sort()

    def _do_jump(self, jump_to, current_index):
        try:
            index = next(index for index, instr in enumerate(self.instructions) if instr.order == jump_to)

            return index
        except StopIteration:
            raise IExc.SemanticIE(
                f'Can not jump by jumping instruction {repr(self.instructions[current_index])}')

    def execute_program(self):
        index = 0
        instr_len = len(self.instructions)

        while index < instr_len:
            instruction = self.instructions[index]
            jump_to = instruction.execute()
            index = index + 1
            if jump_to is not None:
                index = self._do_jump(jump_to, index)

            if isinstance(instruction, Return):
                index = index + 1
