<?php

require_once("TExit.php");


class TNode {
	const interpret = 0;
	const parser = 1;

	private $program_location;
	private $type;

	public function __construct($program_location, $type) {
		$this->program_location = $program_location;
		$this->type = $type;

		if (!file_exists($program_location)) {
			TExit::exit_e(TExit::FILE_ERR, 'Program ' . $program_location . ' not found.');
		}
	}

	public function execute_test($program_source, $program_data_input = "") {
		$program_output = array();
		$program_ec = 0;

		if ($this->type == TNode::interpret) {
			$command = "python3.8 " . $this->program_location .
				" --source=" . $program_source . " --input=" . $program_data_input . " 2>/dev/null ";
		} else {
			$command = "php7.4 " . $this->program_location .
				" < " . $program_source . " 2>/dev/null ";
		}

		$exec_res = exec($command, $program_output, $program_ec);

		$res_arr = array(implode("\n", $program_output), $program_ec);
		return $res_arr;
	}
}


class TChain {
	private $nodes = array();

	const DIFF_M = 0;
	const XML_M = 1;

	private int $diff_method;

	private int $current_return_code = 0;
	private string $current_output = "";

	const OK = 0;
	const RC_FAIL = 1;
	const OUT_FAIL = 2;

	public int $result = 0;
	public string $expected = "";
	public string $result_diff = "";

	public string $XML_comparer_path;

	public function __construct($diff_method, $XML_comparer_path = "/pub/courses/ipp/jexamxml/jexamxml.jar") {
		$this->diff_method = $diff_method;
		$this->XML_comparer_path = $XML_comparer_path;
	}

	public function add_node(TNode $node) {
		array_push($this->nodes, $node);
	}


	private function execute_chain($src, $in) {
		$output = '';
		$exit_code = '';

		foreach ($this->nodes as $node) {
			$result = $node->execute_test($src, $in);
			$output = $result[0];
			$exit_code = $result[1];

			if ($exit_code != 0) {
				$this->current_return_code = $exit_code;
				$this->current_output = $output;
				return;
			}

			$tmp_file_name = "./tmp_src_file.src";
			file_put_contents($tmp_file_name, $output);

			$src = $tmp_file_name;
		}
		$this->current_output = $output;
		$this->current_return_code = $exit_code;
	}

	private function edit_xml_diff($diff) {
		$matches = array();

		preg_match("/JExamXML 1.01 - Java XML comparison tool\nComparing \"[^\"]*\" and \"tmp_output_file\"\n/", $diff, $matches);
		if (count($matches) != 1) return $diff;

		$diff =  substr_replace($diff, '', 0, strlen($matches[0]));

		preg_match("/Two files are not identical$/", $diff, $matches);
		if (count($matches) != 1) return $diff;

		$diff =  substr_replace($diff, '', strlen($diff) - strlen($matches[0]));

		return $diff;
	}

	private function compare_test($out_file, $rc_file) {
		$this->result = TChain::OK;

		// RC
		$rc_handler = fopen($rc_file, "r");
		$expected_rc = trim(fgets($rc_handler));
		fclose($rc_handler);

		if (!is_numeric($expected_rc)) TExit::exit_e(TExit::FILE_ERR, "File " . $rc_file . " doesnt contain return code");

		if ($expected_rc != $this->current_return_code) {
			$this->result = TChain::RC_FAIL;
			$this->expected = strval($expected_rc);
			$this->result_diff = $this->current_return_code;
			return;
		}

		if ($expected_rc != 0 || $this->current_return_code != 0) return;

		$tmp_file_name = "tmp_output_file";
		$tmp_file = fopen($tmp_file_name, 'w');
		fwrite($tmp_file, $this->current_output);
		fclose($tmp_file);

		// OUT
		if ($this->diff_method == TChain::DIFF_M) {
			$command = "diff $out_file $tmp_file_name 2>/dev/null ";
		} else {
			$command = "java -jar  $this->XML_comparer_path $out_file $tmp_file_name /dev/stdout /D ./options  2>/dev/null ;";
		}


		exec($command, $d_out, $d_ec);
		$d_out = implode("\n", $d_out);


		if ($d_ec == 0 or $d_out == "1d0\n<") {
			return;
		}

		if ($this->diff_method == TChain::XML_M and $d_ec == 1) {
			$d_out = $this->edit_xml_diff($d_out);
		}

		$this->result = TChain::OUT_FAIL;
		$this->result_diff = $d_out;
		$this->expected = file_get_contents($out_file);

	}

	public function execute_test(string $src_file, string $in_file, string $out_file, string $rc_file) {
		if (count($this->nodes) == 0) {
			TExit::exit_e(TExit::INTERN_ERR, 'No test nodes');
		}
		$this->execute_chain($src_file, $in_file);

		$this->compare_test($out_file, $rc_file);
	}
}