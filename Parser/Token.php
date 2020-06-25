<?php

/**
 * @author: xmusko00
 * @file Token.php
 * @date 12.2.2019
 */

/**
 * Class Token
 */
abstract class Token
{
    const T_EOF = -1;
    const T_header = 0;
    const T_instr = 2;

    const T_int_const = "int";
    const T_bool_const = "bool";
    const T_string_const = "string";
    const T_nil_const = "nil";
    const T_label = "label";

    const T_type = "type";
    const T_var = "var";

    const T_unknown = 15;

    public $type;
    public $value;

    public function __construct()
    {
        $this->type = Token::T_unknown;
    }


    public function isEOFToken()
    {
        if ($this->type === Token::T_EOF) return true;
        else return false;
    }
}

/**
 * Class TokenLeading
 * Instruction or Header
 */
class TokenLeading extends Token
{
    public function __construct($lex)
    {
        parent::__construct();

        if (Instructions::isInstruction($lex)) {
            $this->type = Token::T_instr;
            $this->value = $lex;
        } else if (strcasecmp($lex, ".IPPcode20") === 0) {
            $this->type = Token::T_header;
        } else {
            $this->type = Token::T_unknown;
            throw new OptCodeException($lex . " is not instruction.");
        }
    }

}

/**
 * Class TokenArgument
 */
class TokenArgument extends Token
{

    public function __construct($lex)
    {
        parent::__construct();

        $this->value = $lex;

        if ("nil@nil" === $lex) {
            $this->type = Token::T_nil_const;
            $this->value = Token::T_nil_const;

        } else if (false !== $suffix = $this->cutPrefix($lex, "int@")) {
            if (is_numeric($suffix)) {
                $this->type = Token::T_int_const;
                $this->value = intval($suffix);
            } else {
                throw new LexOrSyntaxException("No int value after int@");
            }

        } else if (false !== $suffix = $this->cutPrefix($lex, "string@")) {
            $this->type = Token::T_string_const;
            $this->value = $suffix;

        } else if (false !== $suffix = $this->cutPrefix($lex, "bool@")) {
            if ($suffix === "false") {
                $this->type = Token::T_bool_const;
                $this->value = false;
            } else if ($suffix === "true") {
                $this->type = Token::T_bool_const;
                $this->value = true;
            } else {
                throw new LexOrSyntaxException("No int value after int@");
            }

        } else if (substr($lex, 0, "3") === "LF@" ||
            substr($lex, 0, "3") === "GF@" ||
            substr($lex, 0, "3") === "TF@") {
            $this->type = Token::T_var;
            $this->value = $lex;

            $var_name = substr($lex, 3, strlen($lex));

            if (!$this->checkIdentifier($var_name)) {
                $this->type = Token::T_unknown;
                throw new LexOrSyntaxException("Incorrect variable name \"{$var_name}\"");
            }

        } else if ($lex == "string" || $lex == "bool" || $lex == "int") {
            $this->type = Token::T_type;
            $this->value = $lex;

        } else if ($this->checkIdentifier($lex)) {
            $this->type = Token::T_label;
        } else {
            $this->type = Token::T_unknown;
            throw new LexOrSyntaxException("Incorrect identifier");
        }

    }

    private function checkIdentifier($id)
    {
        if (preg_match("/[\w\-$&%*!?]/", $id) === 1) {
            return true;
        }
        return false;
    }

    private function cutPrefix($str, $prefix)
    {
        if ($prefix === substr($str, 0, strlen($prefix)) and strlen($str) > strlen($prefix)) {
            return substr($str, strlen($prefix));
        }
        return false;
    }
}

/**
 * Class TokenEOF
 */
class TokenEOF extends Token
{
    public function __construct()
    {
        parent::__construct();
        $this->type = Token::T_EOF;
    }
}



