<?php

/**
 * @author: xmusko00
 * @file Statistics.php
 * @date 12.2.2019
 */

require_once("Statistics.php");
require_once("lib/BasicEnum-PHP/BasicEnum.php");

abstract class MonItems extends BasicEnum {
	const loc = 'loc';
	const comments = 'comments';
	const labels = 'labels';
	const jumps = 'jumps';
}

class Statistics extends MonItems {
	private $stats_on;
	private $file;

	private $tracked_items_structure = [];
	private $tracked_items;

	/**
	 * Statistics constructor.
	 * @param $on
	 * @param $file
	 * @param MonItems [] $tracked_items_structure
	 */
	public function __construct($on, $file, $tracked_items_structure) {
		$this->stats_on = $on;
		$this->file = $file;
		$this->tracked_items_structure = $tracked_items_structure;

		foreach (MonItems::getAllConstants() as $item) {
			$this->tracked_items[$item] = 0;
		}
	}

	public function incComments() {
		$this->tracked_items[MonItems::comments]++;
	}

	public function incLoc() {
		$this->tracked_items[MonItems::loc]++;
	}

	public function incJumps($str) {
		$jmp = "JUMP";
		if (substr($str, 0, strlen($jmp)) === $jmp) {
			$this->tracked_items[MonItems::jumps]++;
		}
	}

	public function incLabels() {
		$this->tracked_items[MonItems::labels]++;
	}

	public function writeToFile() {
		if(! $this->stats_on) return;

		try {
			$fd = fopen($this->file, 'w');

			foreach ($this->tracked_items_structure as $item) {
				fwrite($fd, $this->tracked_items[$item] . "\n");
			}
			fclose($fd);

		} catch (Exception $e) {
			throw new OutputFileException();
		}
	}
}