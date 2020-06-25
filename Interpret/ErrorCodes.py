OK = 0

PARAM_ERR = 10  # chybějící parametr skriptu (je-li třeba) nebo použití zakázané kombinace parametrů
INPUT_ERR = 11  # chyba při otevírání vstupních souborů
OUTPUT_ERR = 12  # chyba při otevření výstupních souborů pro zápis

SEMANTIC_ERR = 52  # chyba při sémantických kontrolách vstupního kódu v IPPcode20
OP_TYPE_ERR = 53  # špatné typy operandů
NO_VAR_ERR = 54  # přístup k neexistující proměnné
NO_FRAME_ERR = 55  # rámec neexistuje
NO_VALUE_ERR = 56  # chybějící hodnota
OP_VAL_ERR = 57  # špatná hodnota operandu (např. dělení nulou, špatná návratová hodnota instrukce EXIT);
STR_ERR = 58  # chybná práce s řetězcem

INTERN_ERR = 99
