<?php

require_once("TChain.php");

class Result {
	public $test_res = TChain::OK;
	public $name = "";
	public $expected;
	public $diffrence;

	function __construct($name, $test_res, $expected, $diffrence) {
		$this->test_res = $test_res;
		$this->expected = $expected;
		$this->diffrence = $diffrence;
		$this->name = $name;
	}
}

class DirNode {

	public string $directory;
	public $dir_stack = array();
	public $res_stack = array();
	public $total = 0;
	public $totak_ok = 0;

	public string $nickname = "";

	public const NORMAL = 0;
	public const UP = 1;
	public const DOWN = 2;
	public $direction;

	private function get_sub_dirs() {
		$all_sub_dirs = glob($this->directory . '/*', GLOB_ONLYDIR);
		return $all_sub_dirs;

	}

	public function __construct($root, $recursive) {
		if (!is_dir($root)) {
			TExit::exit_e(TExit::FILE_ERR, "Can not find directory " . $root);
		}
		$this->directory = $root;
		$this->direction = DirNode::NORMAL;

		if (!$recursive) return;

		$subdirs = $this->get_sub_dirs();

		if (count($subdirs) == 0) return;

		$this->direction = DirNode::DOWN;

		foreach ($subdirs as $subdir) {
			$new_subdir = new DirNode($subdir, true);
			array_push($this->dir_stack, $new_subdir);
		}

		$last_subdir = end($this->dir_stack);
		$last_subdir->direction = DirNode::UP;
	}

	public function count_results() {
		$this->total = 0;
		$this->totak_ok = 0;

		foreach ($this->res_stack as $res) {
			$this->total++;
			if ($res->test_res == TChain::OK)
				$this->totak_ok++;
		}

		foreach ($this->dir_stack as $subdir) {
			$subdir->count_results();
			$this->total += $subdir->total;
			$this->totak_ok += $subdir->totak_ok;
		}
	}

	public function set_nicknames($add_folder = false) {
		$basename = basename($this->directory);

		$this->nickname = $basename;

		if ($add_folder !== false) {
			$this->nickname = $add_folder . DIRECTORY_SEPARATOR . $basename;
		}

		$subdir_add_folder = false;
		if (count($this->res_stack) == 0) {
			$subdir_add_folder = $this->nickname;
		}

		foreach ($this->dir_stack as $subdir) {
			$subdir->set_nicknames($subdir_add_folder);
		}

	}

	public function add_result($name, $test_res, $expected = "", $diffrence = "") {
		$new_res = new Result($name, $test_res, $expected, $diffrence);
		array_push($this->res_stack, $new_res);
	}

	public function iter_dir_nodes() {
		yield $this;

		foreach ($this->dir_stack as $subdir) {
			$subdir_gen = $subdir->iter_dir_nodes();
			foreach ($subdir_gen as $subsubdir) {
				yield $subsubdir;
			}
		}
	}
}
