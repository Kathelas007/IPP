<?php

/**
 * @author: xmusko00
 * @file InstructionSyntaxAnalysis.php
 * @date 13.2.2019
 */

require_once("LexicalAnalysis.php");
require_once("Statistics.php");
require_once("Instruction.php");
require_once("Token.php");


/**
 * Class InstructionSyntaxAnalysis
 */
class InstructionSyntaxAnalysis {
	private $stat_class = null;

	public function __construct(Statistics $stat_class) {
		$this->stat_class = $stat_class;
	}

	private function isSymbol(Token $t) {
		if ($t->type == Token::T_string_const ||
			$t->type == Token::T_int_const ||
			$t->type == Token::T_bool_const ||
			$t->type == Token::T_nil_const ||
			$this->isVar($t)) {
			return true;
		}
		return false;
	}

	private function isVar(Token $t) {
		if ($t->type == Token::T_var) return true;
		return false;
	}

	private function isLabel(Token $t) {
		if ($t->type == Token::T_label) {
			$this->stat_class->incLabels();
			return true;
		}
		return false;
	}

	private function isType(Token $t) {
		if ($t->type == Token::T_type) return true;
		return false;
	}

	/**
	 * @param Token[] $tokens
	 * @return bool
	 */
	public function checkSyntax(array $tokens) {
		$args_array = $tokens;
		$instr_token = array_shift($args_array);

		$this->stat_class->incJumps($instr_token->value);

		$instr_type = Instructions::getInstructionType($instr_token->value);

		$result = false;
		switch (count($args_array)) {
			case 0:
				if ($instr_type == Instructions::IT_none) $result = true;
				break;
			case 1:
				if (($instr_type == Instructions::IT_var and $this->isVar($args_array[0])) ||
					($instr_type == Instructions::IT_label and $this->isLabel($args_array[0])) ||
					($instr_type == Instructions::IT_symb and $this->isSymbol($args_array[0]))) {
					$result = true;
				}
				break;
			case 2:
				if ($instr_type == Instructions::IT_var_symbol) {
					if ($this->isVar($args_array[0]) and $this->isSymbol($args_array[1]))
						$result = true;
				} elseif ($instr_type == Instructions::IT_var_type) {
					if ($this->isVar($args_array[0]) and $this->isType($args_array[1]))
						$result = true;
				}
				break;
			case 3:
				if ($instr_type == Instructions::IT_var_symb_symb) {
					if ($this->isVar($args_array[0]) and $this->isSymbol($args_array[1]) and $this->isSymbol($args_array[2]))
						$result = true;
				} elseif ($instr_type == Instructions::IT_label_symb_symb) {
					if ($this->isLabel($args_array[0]) and $this->isSymbol($args_array[1]) and $this->isSymbol($args_array[2]))
						$result = true;
				}
				break;
		}
		return $result;
	}
}