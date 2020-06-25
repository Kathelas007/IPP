<?php

/**
 * @author: xmusko00
 * @file LexicalAnalasis.php
 * @date 13.2.2019
 */

require_once("Statistics.php");
require_once("lib/BasicEnum-PHP/BasicEnum.php");
require_once("Instruction.php");
require_once("Token.php");


/**
 * Class LexicalAnalysis
 */
class LexicalAnalysis {
	private $stat_class = null;
	private $file;
	private $current_line;

	private $tokens = [];

	public function __construct($file, Statistics $stat_class) {
		$this->stat_class = $stat_class;
		$this->file = $file;
	}

	public function removeComments() {
		if (false !== $index = strpos($this->current_line, "#")) {
			$this->current_line = substr($this->current_line, 0, $index);
			$this->stat_class->incComments();
		}
	}

	private function addToken($t){
	    array_push($this->tokens, $t);
    }

    private function splitLexeme(){
        return preg_split("/[\s,]+/", $this->current_line, -1, PREG_SPLIT_NO_EMPTY);
    }
    /**
     * Reads from input stream and process Lexical analysis.
     * @return Token [] array of tokens presents one instruction or header
     * @throws LexOrSyntaxException
     * @throws OptCodeException
     */
	public function getTokens() {

		$this->tokens = array();

		while ($this->current_line = fgets(STDIN)) {
			$this->removeComments();
			if (strlen($this->current_line) == 0) continue;

			$lexeme = $this->splitLexeme();
			if (count($lexeme) == 0) continue;

			$this->stat_class->incLoc();

			foreach ($lexeme as $index => $lex) {
					if ($index === 0) $this->addToken(new TokenLeading($lex));
					else $this->addToken(new TokenArgument($lex));

			}
			return $this->tokens;
		}

		$this->addToken(new TokenEOF());
		return $this->tokens;
	}
}