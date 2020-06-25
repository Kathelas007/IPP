"""
author: xmusko00
file: ProgramExit.py
date: 12.3.2019
"""

import sys
import ErrorCodes as EC


class InterpretExit(SystemExit):

    def __init__(self, code=EC.OK, msg=''):
        print(msg, file=sys.stderr)
        super().__init__(code)
