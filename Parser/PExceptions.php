<?php

/**
 * @author: xmusko00
 * @file PExeptions.php
 * @date 20.2.2019
 */

abstract class ProjectExceptions extends Exception{
	public $err_code;
	public $exception_info;

	public function logException(){
		fwrite(STDERR, $this->exception_info . ": \t" . $this->getMessage() . "\n");
	}

	public function logAndExit(){
		$this->logException();
		exit($this->err_code);
	}
}

class ParamException extends ProjectExceptions{
	public $err_code = 10;
	public $exception_info = "Param error";
}


class InputFileException extends ProjectExceptions{
	public $err_code = 11;
	public $exception_info = "Can not read input file";
}

class OutputFileException extends ProjectExceptions{
	public $err_code = 12;
	public $exception_info = "Can not read output file";
}

class BadHeaderException extends ProjectExceptions{
	public $err_code = 21;
	public $exception_info ="Header error";
}

class OptCodeException extends ProjectExceptions{
	public $err_code = 22;
	public $exception_info = "Bad operation code";
}

class LexOrSyntaxException extends ProjectExceptions{
	public $err_code = 23;
	public $exception_info = "Other lex or syntax error";
}

class InternalException extends ProjectExceptions{
	public $err_code = 99;
	public $exception_info = "Internal Error";
}

