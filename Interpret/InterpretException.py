class InterpretException(Exception):
    def __init__(self, code, msg=''):
        self.code = code
        self.msg = msg
        super().__init__(msg)

    def get_code_msg(self):
        return self.code, self.msg


class ParamIE(InterpretException):
    """Chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů"""

    def __init__(self, msg):
        super().__init__(10, msg)


class InputIE(InterpretException):
    """Chyba při otevírání vstupních souborů"""

    def __init__(self, msg):
        super().__init__(11, msg)


class OutputIE(InterpretException):
    """Chyba při otevření výstupních souborů pro zápis"""

    def __init__(self, msg):
        super().__init__(12, msg)


class XMLFormatIE(InterpretException):
    """Chybný XML formát ve vstupním souboru (soubor není tzv. dobře formátovaný, angl. well-formed)"""

    def __init__(self, msg):
        super().__init__(31, msg)


class XMLStructureIE(InterpretException):
    """Neočekávaná struktura XML (např. element pro argument mimo element pro instrukci,
instrukce s duplicitním pořadím nebo záporným pořadím) či lexikální nebo syntaktická chyba
textových elementů a atributů ve vstupním XML souboru (např. chybný lexém pro řetězcový
literál, neznámý operační kód apod.)."""

    def __init__(self, msg):
        super().__init__(32, msg)


class SemanticIE(InterpretException):
    """Chyba při sémantických kontrolách vstupního kódu v IPPcode20"""

    def __init__(self, msg):
        super().__init__(52, msg)


class OperandTypeIE(InterpretException):
    """Špatné typy operandů"""

    def __init__(self, msg):
        super().__init__(53, msg)


class NoVariableIE(InterpretException):
    """Přístup k neexistující proměnné"""

    def __init__(self, msg):
        super().__init__(54, msg)


class NoFrameIE(InterpretException):
    """Rámec neexistuje"""

    def __init__(self, msg):
        super().__init__(55, msg)


class NoValueIE(InterpretException):
    """Chybějící hodnota"""

    def __init__(self, msg):
        super().__init__(56, msg)


class OperandValueIE(InterpretException):
    """Špatná hodnota operandu (např. dělení nulou, špatná návratová hodnota instrukce EXIT);"""

    def __init__(self, msg):
        super().__init__(57, msg)


class StringIE(InterpretException):
    """Chybná práce s řetězcem"""

    def __init__(self, msg):
        super().__init__(58, msg)


class InternIE(InterpretException):
    """Interní chyba"""

    def __init__(self, msg):
        super().__init__(99, msg)
