# Implementační dokumentace k 1. úloze do IPP 2019/2020  
Jméno a příjmení: Kateřina Muškova   
Login: xmusko00

## Struktura programu
Program využívá objektově orientovaného přístup a každá jeho logická část je samostatná třída.  
Hlavní část 'main' se nachází v soubor parse.php, 
a má za úkol spustit ověření argumentů a následně syntaktickou analýzu a výpisy výsledků analýzy.

### Třída StatisticOpts
Tato třída zpracovává vstupní argumenty programu pro účely rozšíření STATS a nápovědu.
Kontroluje jejich strukturu a při chybě vyvolá výjimku, 
přičemž neznámé argumenty nejsou ignorovány, 
ale jsou také považovány za chybu. 

### Třída Parser
Tvoří základní kostru. Po zavolání metody parse() je zkontrolována hlavička a 
následně jednotlivé příkazy programu. 
Obojí se děje na základě pole tokenů získaných z Lexikálního analyzátoru. 
Samotnou syntaktickou kontrolu dané instrukce provádí SyntaxInstructionAnalysis

### Třída LexicalAnalysis
Jediná veřejná funkce getTokens() načítá ze standartního vstupu a 
deleguje vytvoření tokenu na potomky třídy Token, následně vrací pole tokenů, 
které představuje jeden řádek kódu.

### Třída Token
Tato třída obsahuje dva veřejné atributy:  

 * type (label, EOF, instruction, header, string, ...), který je nadmnožinou atributu type elementu argumentu v XML reprezentaci.  
 * value (my_favourit_label, MOVE, IPPcode20, best_string, ...), hodnota některých typů tokenu.  

Další třídy z ní pak dědí:  

 * Třída TokeLeading - instrukce, nebo hlavička  
 * Třída TokenArgument - argument  
 * Třída TokenEOF  

Jako parametry konstruktor dostane lexem, podle kterého buď jde vytvořit daný typ
tokenu, nebo je vyvolána výjimka.

### Třída InstructionSyntaxAnalysis
Tato třída kontroluje syntaxi jednotlivých příkazů (pole tokenů).  
Metoda checkSyntax() zjistí podle prvního tokenu typ instrukce a u ostatních kontroluje, 
zda sedí jako argumenty.

#### Třída Instruction a InstructionType
Instruction dědí od třídy BasicEnum a představuje jen prostý výčet instrukcí, který používá
třída InstructionType pro určení, zda se jedná o instrukci a její typ.  
Obě složí pouze jako pomocné třídy.

### Třída XMLConvertor
XMLConvertor dědí od třídy XMLWriter a rozšířuje její funkcionalitu pro snadný převod IPPcode.
Obsahuje veřejné metody jako startProgram(), writeCommand(), writeOutput(), ...  
Pokud některá z nich potřebuje argumenty, jsou jí opět předány tokeny.

### Třída PException
Kdykoliv se v kódu volá výjimka, je to vždy potomek této třídy.

### Třída Statistics
Na začátku jsou objektu v konstruktoru předány parametry, podle kterých se určí, 
zda má statistické sledování probíhat, popřípadě které položky mají být sledovány atd.
Informaci o zvýšení počtu dané položky předávají ostatní třídy voláním metod 
increase%jmeno_polozky%()


  
