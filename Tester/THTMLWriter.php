<?php

require_once("css_fragments.php");


class THTMLWriter {
	private $document;
	private $header;
	private $summary;

	private function escape_xml_chars(string $text) {
		$text = str_replace('&', '&amp;', $text);
		$text = str_replace('<', '&lt;', $text);
		$text = str_replace('>', '&gt;', $text);
		return $text;
	}

	private function cropp_name(string $name) {
		return substr($name, 0, -4);
	}

	public function start_document() {
		$this->header = doc_begin;
	}

	public function end_document() {
		$bottom = "</body></html> ";
		$this->document .= "$this->header \n\n$this->summary\n\n$bottom \n";
	}

	public function start_header($total_ok, $total, $percent) {
		$this->header .= start_header;

		$this->header .= "<div class=\"box-cell\"><h2> $total_ok </h2>
                <p> succeeded </p></div>";

		$this->header .= " <div class=\"box-cell\"><h2> $total </h2>
                <p> total </p></div>";

		$this->header .= "<div class=\"box-cell\"><h2> $percent </h2>
                <p> % </p></div>";

		$this->header .= "</div></div></div>
				<table class=\"header_info\">";
	}

	public function end_header() {
		$this->header .= "</table> <hr/>";
	}

	public function add_header_info($title, $info) {
		$this->header .= " <tr>
        <td>$title</td>
        <td>$info</td>
    	</tr>";
	}

	public function start_summary() {
		$this->summary .= "<div>\n";

	}

	public function end_summary() {
		$this->summary .= "</div>\n";
	}

	public function start_directory($name, $succeeded, $total) {
		if ($succeeded != $total) {
			$status = "failed";
		} else $status = "ok";

		$this->summary .= "<li> <ul class=\"directory\">
    <div class=\"name $status\"> $name <span>($succeeded/$total)</span></div></li>";
	}

	public function end_directory() {
		$this->summary .= "</ul>";
	}

	public function add_succeeded($name) {
		$name = $this->cropp_name($name);
		$this->summary .= "<li><ul class=\"test\">
            <div class=\"name ok\"> $name</div>
        </ul></li>";
	}

	public function add_failed_output($name, $expected, $difference) {
		$name = $this->cropp_name($name);
		$expected = $this->escape_xml_chars($expected);
		$difference = $this->escape_xml_chars($difference);

		$failed = "    <li><ul class=\"test\">
        <div class=\"name failed\"> $name</div>
        <li class=\"msg\">
            <div class=\"msg_box\">
                <div class=\"expected\">
                    <h4>Expected output</h4>
                    <p>$expected
                    </p>
                </div>
                <div class=\"difference\">
                    <h4>Difference</h4>
                    <p>$difference
                    </p>
                </div>
            </div>
        </li>
    </ul></li>";
		$this->summary .= $failed;

	}

	public function add_failed_rc($name, $expected, $difference) {
		$name = $this->cropp_name($name);

		$failed = "           <li> <ul class=\"test\">
                <div class=\"name failed\"> $name</div>
                <li class=\"msg\">
                    <div class=\"msg_box\">
                    <div class=\"expected\">
                        <h4> Bad return code</h4>
                        <p>Expected return code $expected get $difference</p>
                    </div>
                    </div>
                </li>
            </ul></li>";
		$this->summary .= $failed;
	}


	public function save_document($name) {
		file_put_contents($name . ".HTML", $this->document);
	}
}

function my_main() {
	$writer = new THTMLWriter();
	$writer->start_document();

	$writer->start_header(2, 3, 60);
	$writer->add_header_info('date', '10.10.2010');
	$writer->add_header_info('recursive', 'Yes');
	$writer->end_header();

	$writer->start_summary();


	$writer->start_directory('folder uno', 3, 4);
	$writer->add_succeeded("velmi uspesny test");
	$writer->add_succeeded("druhy uspesny test");
	$writer->add_succeeded("druhy uspesny test");
	$writer->add_failed_output("baaad test", "aaa\na", "no new line");
	$writer->end_directory();

	$writer->end_summary();

	$writer->end_document();
	$writer->save_document('result');

}




