<?php

/**
 * @author: xmusko00
 * @file XMLConvertor.php
 * @date 25.2.2019
 */

/**
 * Class XMLConverter
 */
class XMLConverter extends XMLWriter {
	private $count = 1;

	public function __construct() {
		$this->openMemory();
		$this->setIndent(true);
	}

	public function startProgram() {
		$this->startDocument('1.0', 'UTF-8');
		$this->startElement("program");
		$this->writeAttribute("language", "IPPcode20");
	}

	private function writeText($text) {
		$text = str_replace("&", "&amp;", $text);
		$text = str_replace("<", "&lt;", $text);
		$text = str_replace(">", "&gt;", $text);
		$this->writeRaw($text);
	}

	private function writeArgument(Token $arg, $index) {
		$arg_name = "arg" . strval($index+1);
		$this->startElement($arg_name);

		$this->writeAttribute("type", $arg->type);
		$this->writeText($arg->value);

		$this->endElement();
	}

	private function writeOrderAttribute() {
		$count = strval($this->count);
		$this->count++;
		$this->writeAttribute("order", $count);
	}

	public function writeCommand(Token $command, $c_args) {
		$this->startElement("instruction");
		$this->writeOrderAttribute();
		$this->writeAttribute("opcode", $command->value);

		foreach ($c_args as $index => $c_arg) {
			$this->writeArgument($c_arg, $index);
		}
		$this->endElement();
	}

	public function endProgram() {
		$this->endElement();
		$this->endDocument();
	}

	public function writeOutput() {
		return $this->outputMemory();
	}
}