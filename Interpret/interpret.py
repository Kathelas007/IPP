"""
author: xmusko00
file: interpret.py
date: 12.3.2019
"""


import sys
import getopt

from InterpretExit import InterpretExit as IExit
from InterpretException import InterpretException as IExc
from Argument import ArgumentBuilder
from Instruction import InstructionBuilder
from IPPMemory import IPPMemory
from IPPParser import IPPParser
from Program import Program
import ErrorCodes as EC


def parse_args():
    p_args_err_code = 10
    help_msg = """Interpreter

    usage:
    -h, --help       show this help message and exit
    
    --source         source file with XML
    --input          program input
    """

    long_opts = 'help source= input='

    try:
        options, remainder = getopt.getopt(sys.argv[1:], '', long_opts.split())
    except getopt.GetoptError as e:
        raise IExit(p_args_err_code, e.msg)

    options = {opt: val for opt, val in options}
    a_source = a_input = None

    if '--help' in options:
        print(help_msg)

        if len(options) != 1:
            raise IExit(p_args_err_code, 'Help must stay alone')
        else:
            raise IExit()

    if '--source' in options:
        a_source = options['--source']

    if '--input' in options:
        a_input = options['--input']

    if a_input is None and a_source is None:
        print(help_msg)
        raise IExit(p_args_err_code, 'At least one of --source or --input argument is expected.')

    return a_source, a_input


def get_source_contend(file_name):
    if not file_name:
        return sys.stdin.readlines()
    try:
        with open(file_name) as f:
            return f.readlines()
    except IOError:
        raise IExit(EC.INPUT_ERR, f"Can not read input file {file_name}")


def redirect_stdin(input_filename):
    original = sys.stdin
    if input_filename:
        try:
            sys.stdin = open(input_filename)
        except IOError:
            raise IExit(EC.INPUT_ERR, "Can not open input file")
    return original


def restore_stdin(original_stdin):
    sys.stdin = original_stdin


def feed_program(program, parser, mem):
    arg_builder = ArgumentBuilder(mem)
    inst_builder = InstructionBuilder(mem)

    program.start_instruction_init()

    try:
        parser.parse()
        for instruction_info in parser.iter_instructions():
            arguments = [arg_builder.create(*arg) for arg in list(parser.iter_arguments())]
            instruction_obj = inst_builder.create_instr(instruction_info[0], instruction_info[1], arguments)
            program.add_instruction(instruction_obj)

        program.end_instruction_init()
    except IExc as exc:
        raise IExit(*(exc.get_code_msg()))


def execute_program(program, input_filename):
    original_stdin = redirect_stdin(input_filename)
    try:
        program.execute_program()
    except IExc as exc:
        raise IExit(*(exc.get_code_msg()))
    finally:
        restore_stdin(original_stdin)


def main():
    src_filename, input_filename = parse_args()
    xml_file_contend = get_source_contend(src_filename)

    parser = IPPParser(xml_file_contend)
    mem = IPPMemory()
    program = Program(mem)

    feed_program(program, parser, mem)

    execute_program(program, input_filename)


if __name__ == "__main__":
    main()
