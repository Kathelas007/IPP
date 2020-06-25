<?php
require_once("TSetting.php");
require_once("TChain.php");
require_once("THTMLWriter.php");
require_once("TIterDirectory.php");

function set_chain_nodes(TChain &$Chain, TSetting &$Setting) {

	if ($Setting->test_mode == TSetting::PAR_ONLY) {
		$node = new TNode($Setting->parse_script, TNode::parser);
		$Chain->add_node($node);
	} elseif ($Setting->test_mode == TSetting::INT_ONLY) {
		$node = new TNode($Setting->int_script, TNode::interpret);
		$Chain->add_node($node);
	} else {
		$node_p = new TNode($Setting->parse_script, TNode::parser);
		$node_i = new TNode($Setting->int_script, TNode::interpret);
		$Chain->add_node($node_p);
		$Chain->add_node($node_i);
	}
}


function search_dirs($root_dir, $recursive) {
	if (!is_dir($root_dir)) {
		TExit::exit_e(TExit::FILE_ERR, "Can not find directory " . $root_dir);
	}

	if (!$recursive) {
		yield $root_dir;
	} else {

		$to_exclude1 = $root_dir . '/..';
		$to_exclude2 = $root_dir . '..';

		$dir_iter = new RecursiveIteratorIterator(new RecursiveDirectoryIterator($root_dir),
			RecursiveIteratorIterator::SELF_FIRST | RecursiveDirectoryIterator::SKIP_DOTS);
		foreach ($dir_iter as $dir_path) {
			if ($dir_path->isDir()) {
				$return_path = $dir_path->__toString();

				if ($return_path != $to_exclude1 and $return_path != $to_exclude2) {
					yield $return_path;
				}
			}
		}
	}
}

function get_src_files($dir) {
	$all_files = scandir($dir);
	$all_files = array_diff($all_files, array('.', '..'));

	$ret_files = array();

	foreach ($all_files as $file) {

		if (is_file($dir . DIRECTORY_SEPARATOR . $file) and strlen($file) > 5 and substr($file, strlen($file) - 4, strlen($file) - 1) == ".src") {
			array_push($ret_files, $file);
		}
	}
	return $ret_files;
}

// src, in, out, rc
function get_other_files($dir, $src_file) {
	$all_files = array();
	$src_file = $dir . DIRECTORY_SEPARATOR . $src_file;

	array_push($all_files, $src_file);

	$replacements = array('in', 'out');
	foreach ($replacements as $replace) {
		array_push($all_files, substr_replace($src_file, $replace, strlen($src_file) - 3));
	}

	//	create empty in, out if needed
	foreach ($all_files as $file) {
		$opened_file = fopen($file, 'c+');
		if (!$opened_file) {
			TExit::exit_e(TExit::FILE_ERR, 'Can not open ' . $file);
		}
		fclose($opened_file);
	}

	// create rc with 0 if needed
	$rc_file = substr_replace($src_file, 'rc', strlen($src_file) - 3);
	$exists = is_file($rc_file);

	$opened_file = fopen($rc_file, 'c+');
	if (!$opened_file) {
		TExit::exit_e(TExit::FILE_ERR, 'Can not open ' . $rc_file);
	}
	if (!$exists) fwrite($opened_file, '0');

	fclose($opened_file);

	array_push($all_files, $rc_file);

	return $all_files;

}

function add_header_info(THTMLWriter $Writer, TSetting $Setting, $total_succ, $total) {
	$percent = (int)((100 * $total_succ) / $total);

	$Writer->start_header($total_succ,  $total, $percent);
	$Writer->add_header_info("Date", date("d/m/Y"));

	if ($Setting->recursive) $recursive = "yes";
	else $recursive = "no";
	$Writer->add_header_info("Recursive", $recursive);

	$Writer->add_header_info("Test directory", $Setting->directory);

	if ($Setting->test_mode == TSetting::PAR_ONLY) {
		$Writer->add_header_info("Parser", $Setting->parse_script);
	} elseif ($Setting->test_mode == TSetting::INT_ONLY) {
		$Writer->add_header_info("Interpret", $Setting->int_script);
	} else {
		$Writer->add_header_info("Parser", $Setting->parse_script);
		$Writer->add_header_info("Interpret", $Setting->int_script);
	}

	$Writer->end_header();
}

function test_res_to_dir_nodes(TChain $Chain, $dir_node_generator) {
	foreach ($dir_node_generator as $dir_node) {

		$files = get_src_files($dir_node->directory);
		foreach ($files as $file) {
			$src_in_out_rc = get_other_files($dir_node->directory, $file);
			$Chain->execute_test($src_in_out_rc[0], $src_in_out_rc[1], $src_in_out_rc[2], $src_in_out_rc[3]);
			$dir_node->add_result($file, $Chain->result, $Chain->expected, $Chain->result_diff);
		}
	}
}

function res_to_html_summary(THTMLWriter $Writer, DirNode $root_directory_node) {
	$Writer->start_summary();

	$dir_node_generator = $root_directory_node->iter_dir_nodes();
	foreach ($dir_node_generator as $dir_node) {
		if (count($dir_node->res_stack) == 0) continue;

		$Writer->start_directory($dir_node->nickname, $dir_node->totak_ok, $dir_node->total);

		foreach ($dir_node->res_stack as $result) {
			if ($result->test_res == TChain::OK) {
				$Writer->add_succeeded($result->name);
			} elseif ($result->test_res == TChain::RC_FAIL) {
				$Writer->add_failed_rc($result->name, $result->expected, $result->diffrence);
			} elseif ($result->test_res == TChain::OUT_FAIL) {
				$Writer->add_failed_output($result->name, $result->expected, $result->diffrence);
			}
		}

		if ($dir_node->direction == DirNode::NORMAL) {
			$Writer->end_directory();
		} elseif ($dir_node->direction == DirNode::UP) {
			$Writer->end_directory();
			$Writer->end_directory();
		}
	}

	$Writer->end_summary();
}

function main() {
	$Setting = new TSetting();
	$Setting->set_configuration();

	if ($Setting->test_mode == TSetting::PAR_ONLY) $Chain = new TChain(TChain::XML_M, $Setting->jexamxml);
	else $Chain = new TChain(TChain::DIFF_M);
	set_chain_nodes($Chain, $Setting);

	$root_directory_node = new DirNode($Setting->directory, $Setting->recursive);
	$dir_node_generator = $root_directory_node->iter_dir_nodes();

	test_res_to_dir_nodes($Chain, $dir_node_generator);
	$root_directory_node->count_results();
	$root_directory_node->set_nicknames(false);

	$Writer = new THTMLWriter();
	$Writer->start_document();

	res_to_html_summary($Writer, $root_directory_node);

	add_header_info($Writer, $Setting, $root_directory_node->totak_ok, $root_directory_node->total);

	$Writer->end_document();
	$Writer->save_document('result');
}

main();