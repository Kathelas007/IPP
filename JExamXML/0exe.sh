echo '<?xml version="1.0" encoding="UTF-8"?>
<program language="IPPcode20">
 <instruction order="1" opcode="DEFVAR">
  <arg1 type="var">GF@a</arg1>
 </instruction>
 <instruction order="2" opcode="READ">
  <arg1 type="var">GF@a</arg1>
  <arg2 type="type">int</arg2>
 </instruction>
 <instruction order="3" opcode="WRITE">
  <arg1 type="var">GF@a</arg1>
 </instruction>
 <instruction order="4" opcode="WRITE">
  <arg1 type="string">\032&lt;not-tag/&gt;\032</arg1>
 </instruction>
 <instruction order="5" opcode="WRITE">
  <arg1 type="bool">1</arg1>
 </instruction>
</program>
' | java -jar  /home/awesomenickname/FIT/IPP/IPP_proj/JExamXML/jexamxml.jar /home/awesomenickname/FIT/IPP/IPP_proj/Testy/ipp-2020-tests/parse-only/basic/read_test.out  /dev/stdin /dev/stdout /D ./options ;
