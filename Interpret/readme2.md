# Implementační dokumentace ke 2. úloze do IPP 2019/2020  
Jméno a příjmení: Kateřina Mušková   
Login: xmusko00

## Interpret

### Struktura programu
Script využívá objektově orientovaného přístupu a každá jeho logická část je samostatná třída, nebo soubor. Každá tato část má svůj UnitTest.

Hlavní část 'main' nacházející se v souboru interpret.py 
má za úkol zpracovat argumenty programu a naplnit pomocí IPPParseru Program, který následně 'spustí'.

#### Třída IPPParser
IPP parser zpracovává a kontroluje vstupní XML soubor. Pro přístup k informacím o argumentech a instrukcích slouží generátory `iter_arguments()` a `iter_instructions()`.

#### Soubor Argument
Obsahuje všechny třídy, které mohou představovat Argument. Jsou tu dvě abstraktní nadtřídy `Symbol` a `Constant`, ze kterých dědí konkrétní třídy jako `Variable`, `Int`, ...
K vytvoření daného Argumentu slouží `ArgBuilder`.

Třída `Variable` má navíc přístup k IPPMemory.

#### Soubor Instruction
Obsahuje opět všechny třídy, které mohou představovat Instrukci. Každá konkrétní instrukce (`Sub`, `Or`, ...) dědí od abstraktní třídy `Instruction` (definuje abstraktní metodu `execute()`) a od potomka třídy `InstructionType` - NoArgI, SymI, VarSymI, atd., který volá metodu `check_args(arg_classes, args)`. 

K vytvoření dané instrukce slouží `InstructioBuilder`.

#### Třída Program
Po naplnění instrukcemi do seznamu, jsou tyto instrukce postupně vykonávány. Skok znamená pouze změnu aktuálního indexu seznamu.

#### Třída IPPMemory
Jakákoliv data, se kterými instrukce pracují jsou uložena v instanci třídy IPPMemory. Obsahuje datový zásobník, zásobník rámců, globální a dočasný zásobník s příslušnými hodnotami proměnných. 

## Tester

### Struktura programu
Script využívá objektově orientovaného přístupu a každá jeho logická část je samostatná třída, nebo soubor.  

Hlavní část 'main' se nacházející se v souboru test.py, 
má za úkol zpracovat argumenty programu, spustit porovnávání a zajistit generování výsledného reportu.

#### Třída TSetting
Má na starosti zpracování vstupních argumentů a jejich validaci.

#### Soubor TIterDirectory
Obsahuje především třídu DirNode. Pokud je při inicializaci argument `$recursive` nastaven na true, vytváří si každá instance pole instancí přímých podadresářů. Jakákoliv operace nad kořenovým uzlem je pak provedena i na synech.
 
Do DirNode jsou ukládány i výsledky testů kvůli lepší manipulaci a přehlednosti. 

#### Třída TChain
Řetězec testovaných programů. Výstup testu jednoho programu je předán jako vstup dalšího. Konečný výsledek je porovnán předem učenou metodou. 

#### Třída THTMLWriter
Umožňuje vytvářet výsledný HTML výstup. Obsahuje metody jako `start_summary()`,  `start_directory($name, $succeeded, $total)`, `add_succeeded($name)`, ...
