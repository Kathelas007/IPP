# todo testing
# todo exit codes

import xml.etree.ElementTree as ET
import re

import InterpretException as IExc


class IPPParser:
    PROG_EL = 'program'
    LANG_ATT = 'language'
    LANG_VAL = 'IPPcode20'
    NAME_ATT = 'name'
    DESC_ATT = 'description'

    INST_EL = 'instruction'
    OP_CODE_ATT = 'opcode'
    ORDER_ATT = 'order'

    ARG_EL = 'arg'
    TYPE_ATT = 'type'

    def __init__(self, xml_document: list):
        self.root: ET.Element
        self.program: ET.Element
        self.current_instruction: ET.Element
        self.document: list = xml_document

    def check_header(self):
        if not self.document:
            return None

        first_line = self.document[0]
        # name tu muze byt
        return (re.match('^\s*<\?xml\s+version="1.0"\s+encoding="UTF-8"\s*\?>$', first_line) or
                re.match('^\s*<\?xml\s+version="1.0"\s+encoding="UTF-8"\s*name="[\w]"\?>$', first_line))

    def parse(self):
        if not self.check_header():
            raise IExc.XMLStructureIE('No header.')

        try:
            self.root = ET.fromstringlist(self.document)
        except ET.ParseError:
            raise IExc.XMLFormatIE('xml.etree.ElementTree ')

        if self.root.tag != self.PROG_EL:
            raise IExc.XMLStructureIE('Bad or missing program tag')

        root_attributes = self.root.attrib
        root_attributes.pop(self.NAME_ATT, None)
        root_attributes.pop(self.DESC_ATT, None)

        if root_attributes.get(self.LANG_ATT) != self.LANG_VAL or len(root_attributes) != 1:
            raise IExc.XMLStructureIE('Bad or missing program attributes')

    def iter_instructions(self):
        """ Yields instruction (order and operation code of instruction)"""
        order_num_list = []

        for instruction in list(self.root):
            if instruction.tag != self.INST_EL:
                raise IExc.XMLStructureIE('No instruction tag')

            attributes = instruction.attrib
            if not (self.OP_CODE_ATT in attributes and self.ORDER_ATT in attributes) or len(attributes) != 2:
                raise IExc.XMLStructureIE('Bad attributes by instruction')

            self.current_instruction = instruction

            order = attributes[self.ORDER_ATT]
            opcode = attributes[self.OP_CODE_ATT].upper()

            if not order or not opcode:
                raise IExc.XMLStructureIE("No order or opcode by ")

            if not order.isnumeric():
                raise IExc.XMLStructureIE("Order must be digit")

            order = int(order)

            if order in order_num_list:
                raise IExc.XMLStructureIE("Order of instructions must be uniq")
            if order <= 0:
                raise IExc.XMLStructureIE("Order must be bigger then 0")

            order_num_list.append(order)

            yield order, opcode

    def _add_arg_to_dict(self, argument, args_dict):
        if self.ARG_EL != argument.tag[0:-1]:
            raise IExc.XMLStructureIE(f'Argument tag argX expected')

        arg_index = argument.tag[-1]
        if not arg_index.isnumeric():
            raise IExc.XMLStructureIE('Argument tag argX expected, where X = {1, 2, 3}')

        arg_index = int(arg_index)
        if arg_index not in {1, 2, 3}:
            raise IExc.XMLStructureIE('Argument tag argX expected, where X = {1, 2, 3}')

        attributes = argument.attrib

        # ak = list(attributes.keys())
        # if ak != ['type']:
        #     raise IExc.XMLStructureIE(f'Type argument expected.')

        if not (self.TYPE_ATT in attributes and len(attributes) == 1):
            raise IExc.XMLStructureIE('Only type attribute expected')

        if (arg_index - 1) in args_dict:
            raise IExc.XMLStructureIE('Argument tag number must be uniq')

        if argument.text is None:
            raise IExc.XMLStructureIE('Text in argument expected')

        args_dict[arg_index - 1] = (attributes[self.TYPE_ATT], argument.text)

        return args_dict

    def iter_arguments(self):
        """ Yields argument (type and value)"""
        args_dict = {}

        for _, argument in enumerate(list(self.current_instruction)):
            args_dict = self._add_arg_to_dict(argument, args_dict)

        args_dict = {key: args_dict[key] for key in sorted(args_dict.keys())}

        if len(args_dict) != 0:
            all_args_exists = all(i in args_dict for i in range(0, len(args_dict)))
            if not all_args_exists:
                raise IExc.XMLStructureIE('Argument tag argX expected, where X = {1, 2, 3}')

        for _, arg in args_dict.items():
            yield arg
