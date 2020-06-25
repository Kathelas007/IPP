<?php


class TExit {
	const OK = 0;
	const PARAM_ERR = 10;
	const FILE_ERR = 11;
	const FILE_WRITE_ERR = 12;
	const INTERN_ERR = 99;

	public static function exit_e($err_code = TExit::OK, $msg = '') {
		fwrite(STDERR, $msg);
		exit($err_code);
	}
}