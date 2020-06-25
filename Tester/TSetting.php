<?php

require_once("TExit.php");


class TSetting {
	private $help = "IPP TESTER - tests Parser and Interpreter

	--help					help
	
	--directory=path		directory with tests, by default current directory
	--recursive 			search recursively in directory
	
	--parse-script=file		file with parse script, by default file parse.php in current directory expected
	--int-script=file		file with interpret script, by default file interpret.php in current directory expected
	--parse-only			test parser only
	--int-only				test interpret only
	--jexamxml=file			file with JAR package with A7Soft JExamXM, by default /pub/courses/ipp/jexamxml/jexamxml.jar expected
	";


	private $opts;

	public $directory;
	public $recursive;
	public $parse_script;
	public $int_script;
	public $test_mode;
	public $jexamxml;

	const BOTH = 0;
	const PAR_ONLY = 1;
	const INT_ONLY = 2;

	private function parse_opts() {
		$long_opts = array(
			"help",
			"directory:",
			"recursive",
			"parse-script:",
			"int-script:",
			"parse-only",
			"int-only",
			"jexamxml:"
		);

		$this->opts = getopt("", $long_opts);

	}

	private function validate_opts() {
		if (array_key_exists('help', $this->opts)) {
			if (count($this->opts) != 1) {
				TExit::exit_e(TExit::PARAM_ERR, 'Help must stay alone');
			} else {
				TExit::exit_e();
			}
		}

		if (array_key_exists('parse-only', $this->opts) and array_key_exists('int-only', $this->opts)) {
			TExit::exit_e(TExit::PARAM_ERR, 'Arguments --parse-only and --int-only can not be together.');
		}
	}

	private function get_opt_key_value($key_a, $value_req) {
		$key = false;
		$value = false;

		if (array_key_exists($key_a, $this->opts)) {
			$key = true;
			$value = $this->opts[$key_a];

			if ($value_req and $value == false) {
				TExit::exit_e(TExit::PARAM_ERR, 'No value by argument ' . $key_a);

			} elseif ($value_req and $value) {
				return $value;

			} elseif ($value_req == false and $value) {
				TExit::exit_e(TExit::PARAM_ERR, 'Argument ' . $key_a . ' does not require value');

			} elseif ($value_req == false and $value == false) {
				return true;
			}
		}
		return false;
	}

	private function set_properties() {
		$this->directory = getcwd();
		$this->recursive = false;
		$this->parse_script = realpath('./parse.php');
		$this->int_script = realpath('./interpret.php');
		$this->test_mode = TSetting::BOTH;
		$this->jexamxml = realpath('./pub/courses/ipp/jexamxml/jexamxml.jar');


		$directory = $this->get_opt_key_value('directory', true);
		if ($directory) $this->directory = realpath($directory);

		$this->recursive = $this->get_opt_key_value('recursive', false);

		$parse = $this->get_opt_key_value('parse-script', true);
		if ($parse) $this->parse_script = realpath($parse);

		$int = $this->get_opt_key_value('int-script', true);
		if ($int) $this->int_script = realpath($int);

		$mode = $this->get_opt_key_value('int-only', false);
		if ($mode) $this->test_mode = TSetting::INT_ONLY;

		$mode = $this->get_opt_key_value('parse-only', false);
		if ($mode) $this->test_mode = TSetting::PAR_ONLY;

		$jar = $this->get_opt_key_value('jexamxml', true);
		if ($jar) $this->jexamxml = realpath($jar);
	}

	public function format_dir(){
		if (! is_dir($this->directory)){
			TExit::exit_e(TExit::FILE_ERR, "Can not find directory " . $this->directory);
		}

		$this->directory = realpath($this->directory);
	}

	public function set_configuration() {
		$this->parse_opts();
		$this->validate_opts();
		$this->set_properties();

		$this->format_dir();
	}

	public function print_attributes(){
		echo 'directory: ' . $this->directory . "\n";
		print 'recursive: ' . $this->recursive. "\n";
		print 'parse_script: ' . $this->parse_script. "\n";
		print 'int_script: ' . $this->int_script. "\n";
		print 'test_mode: ' . $this->test_mode. "\n";
		print 'jexaxml: ' . $this->jexamxml. "\n";
	}

}