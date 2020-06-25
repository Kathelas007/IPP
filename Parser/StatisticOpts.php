<?php

/**
 * @author: xmusko00
 * @file GetOpts.php
 * @date 12.2.2019
 */

/**
 * Class GetStatOpts
 * Class process, parse and check all arguments for statistic purposes and help option
 * All stats options are available after calling method parseArgs()
 */
Class StatisticOpts
{
    private $opts = [];
    private $stat_mode = false;
    private $file = "";
    private $monitored_items_structure = [];
    private $all_items = [];

    private $isHelp = false;

    public function __construct($enum)
    {
        $this->all_items = $enum;
    }

    public function printHelp()
    {
        fprintf(STDOUT, "Parser
		--help			help
		
		--stats=file	statistic mode, monitored items are printed to file
		--loc			number of lines with commands
		--jumps			number of lines with jumps
		--labels		number of labels
		--comments		number of comments
		");
    }

    private function argv2optArray(array $a)
    {
        $opts = [];
        foreach ($a as $value) {
            if (substr($value, 0, 2) != "--") {
                throw new ParamException("Long opts only");
            } else {
                array_push($opts, substr($value, 2, strlen($value)));
            }
        }
        return $opts;
    }

    private function checkHelp()
    {

        if (in_array("help", $this->opts)) {
            if (count($this->opts) != 1) {
                throw new ParamException("Help must stay alone");
            } else {
                $this->isHelp = true;
                $this->printHelp();
            }
        }
    }

    private function checkAndSetStats()
    {
        if (count($this->opts) == 0) {
            return;
        }

        $stat = "stats=";
        $found = false;

        foreach ($this->opts as $opt) {
            if (substr($opt, 0, strlen($stat)) == $stat) {
                # stats
                $found = true;
                $this->stat_mode = true;
                $this->file = substr($opt, strlen($stat));

            } else {
                if (in_array($opt, $this->all_items)) {
                    array_push($this->monitored_items_structure, $opt);
                } else {
                    throw new ParamException("Unknown argument.");
                }
            }
        }

        if (!$found) {
            throw new ParamException("No stats argument.");
        }
    }

    public function parseArgs()
    {
        global $argv;
        $parsed_args = $argv;
        array_shift($parsed_args);

        $this->opts = $this->argv2optArray($parsed_args);

        # can end here
        $this->checkHelp();
        if (!$this->isHelp) {
            $this->checkAndSetStats();
        }
    }

    public function getStatMode()
    {
        return $this->stat_mode;
    }

    public function getFile()
    {
        return $this->file;
    }

    public function getMonItemsStructure()
    {
        return $this->monitored_items_structure;
    }

    public function isHelp()
    {
        return $this->isHelp;
    }
}