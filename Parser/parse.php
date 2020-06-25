#!/usr/bin/php
<?php

/**
 * @author: xmusko00
 * @file parse.php
 * @date 12.2.2019
 */

require_once("StatisticOpts.php");
require_once("Statistics.php");
require_once("LexicalAnalysis.php");
require_once("Token.php");
require_once("InstructionSyntaxAnalysis.php");
require_once("XMLConverter.php");
require_once("PExceptions.php");


/**
 * Class Parser
 * Process syntactic analysis, runs
 * @property $Stats : Statistics
 * @property $Lex : LexicalAnalysis
 * @property $Syn : InstructionSyntaxAnalysis
 * @property $Converter : XMLConverter
 */
class Parser {
	private $file;
	private $Stats = null;
	private $Lex = null;
	private $Syn = null;
	private $Converter = null;


	public function __construct($file, Statistics $Stats) {
		$this->file = $file;
		$this->Stats = $Stats;
	}

	private function isNotEOF(Token $t){
		return ! $t->isEOFToken();
	}

	private function checkHeader(){
        $tokens = $this->Lex->getTokens();
        if (count($tokens) != 1 or $tokens[0]->type !== Token::T_header){
            throw new BadHeaderException("Missing header");
        }
    }

    private function checkProgram(){
        $tokens = $this->Lex->getTokens();
        while (array_key_exists(0, $tokens) and $this->isNotEOF($tokens[0])) {
            if ($this->Syn->checkSyntax($tokens) === false){
                throw new LexOrSyntaxException("Syntax error");
            }

            $command_token = array_shift($tokens);
            $this->Converter->writeCommand($command_token, $tokens);

            $tokens = $this->Lex->getTokens();
        }
    }


    public function writeOutput(){
        echo $this->Converter->writeOutput();
    }

    public function writeStatistics(){
        $this->Stats->writeToFile();
    }

    /**
     * @throws BadHeaderException
     * @throws LexOrSyntaxException
     */
	public function parse() {
		$this->Lex = new LexicalAnalysis($this->file, $this->Stats);
        $this->Syn = new InstructionSyntaxAnalysis($this->Stats);
        $this->Converter = new XMLConverter();

		$this->checkHeader();

        $this->Converter->startProgram();

        $this->checkProgram();

        $this->Converter->endProgram();

	}
}

/*************************************
			MAIN                    */

$Opts = new StatisticOpts(MonItems::getAllConstants());

try {
	$Opts->parseArgs();
} catch (ParamException $e) {
	$Opts->printHelp();
	$e->logAndExit();
}

if($Opts->isHelp()){
	exit(0);
}

$Stats = new Statistics($Opts->getStatMode(), $Opts->getFile(), $Opts->getMonItemsStructure());
$Parser = new Parser($Opts->getFile(), $Stats);

try{
	$Parser->parse();
} catch (ProjectExceptions $e){
	$e->logAndExit();
}

$Parser->writeOutput();

try{
    $Parser->writeStatistics();
} catch (ProjectExceptions $e){
    $e->logAndExit();
}

exit(0);

