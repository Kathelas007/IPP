<?php

/**
 * @author: xmusko00
 * @file Instruction.php
 * @date 14.2.2019
 */

require_once("lib/BasicEnum-PHP/BasicEnum.php");


abstract class InstructionEnum extends BasicEnum {
	const I_move = "MOVE";
	const I_create_f = "CREATEFRAME";
	const I_push_f = "PUSHFRAME";
	const I_pop_f = "POPFRAME";
	const I_def_var = "DEFVAR";
	const I_call = "CALL";
	const I_ret = "RETURN";

	const I_pushs = "PUSHS";
	const I_pops = "POPS";
	const I_add = "ADD";
	const I_sub = "SUB";
	const I_mul = "MUL";
	const I_idiv = "IDIV";
	const I_lt = "LT";
	const I_gt = "GT";
	const I_eq = "EQ";
	const I_and = "AND";
	const I_or = "OR";
	const I_not = "NOT";
	const I_int2char = "INT2CHAR";
	const I_str2int = "STRI2INT";

	const I_read = "READ";
	const I_write = "WRITE";

	const I_concat = "CONCAT";
	const I_strlen = "STRLEN";
	const I_getchar = "GETCHAR";
	const I_setchar = "SETCHAR";

	const I_type = "TYPE";

	const I_label = "LABEL";
	const I_jump = "JUMP";
	const I_jumpifeq = "JUMPIFEQ";
	const I_jumpifneq = "JUMPIFNEQ";
	const I_exit = "EXIT";

	const I_dprint = "DPRINT";
	const I_break = "BREAK";
}

abstract class Instructions extends InstructionEnum {
	const IT_none = 0;
	const IT_var = 1;
	const IT_label = 2;
	const IT_symb = 3;
	const IT_var_symbol = 4;
	const IT_var_type = 5;
	const IT_var_symb_symb = 6;
	const IT_label_symb_symb = 7;

	private static $type_array = array(
		self::IT_none => [InstructionEnum::I_create_f, InstructionEnum::I_push_f, InstructionEnum::I_pop_f, InstructionEnum::I_ret, InstructionEnum::I_break],
		self::IT_var => [InstructionEnum::I_def_var, InstructionEnum::I_pops],
		self::IT_label => [InstructionEnum::I_call, InstructionEnum::I_label, InstructionEnum::I_jump],
		self::IT_symb => [InstructionEnum::I_pushs, InstructionEnum::I_write, InstructionEnum::I_exit, InstructionEnum::I_dprint],
		self::IT_var_symbol => [InstructionEnum::I_move, InstructionEnum::I_int2char, InstructionEnum::I_strlen, InstructionEnum::I_type],
		self::IT_var_type => [InstructionEnum::I_read],
		self::IT_var_symb_symb => [InstructionEnum::I_add, InstructionEnum::I_sub, InstructionEnum::I_mul, InstructionEnum::I_idiv,
			InstructionEnum::I_lt, InstructionEnum::I_gt, InstructionEnum::I_eq,
			InstructionEnum::I_and, InstructionEnum::I_or, InstructionEnum::I_not, InstructionEnum::I_str2int,
			InstructionEnum::I_concat, self::I_getchar, InstructionEnum::I_setchar],
		self::IT_label_symb_symb => [InstructionEnum::I_jumpifeq, InstructionEnum::I_jumpifneq]
	);


	public static function isInstruction($str) {

		return InstructionEnum::isValidValue(strtoupper($str));
	}

	public static function getInstructionType($str){
		foreach (Instructions::$type_array as $type => $types){
			if (in_array(strtoupper($str), $types)){
				return $type;
			}
		}
		return false;
	}
}