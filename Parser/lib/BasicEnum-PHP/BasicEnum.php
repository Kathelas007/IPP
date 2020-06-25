<?php
/**
 * BasicEnum
 *
 * @author Brian Gebel <brian@pixeloven.com>
 * @link https://github.com/pixeloven/BasicEnum-PHP
 * @copyright 2015 PixelOven (Under MIT License)
 *
 * Allows for basic enumeration in PHP
 * 
 */

abstract class BasicEnum {

	// Static Variables
	private static $constCacheArray = NULL;

	/**
	 * Checks if name exists in enum
	 * @param: (string)
	 * @param: (bool)
	 * @return: (bool)
	 */
	public static function isValidName($name, $strict = false) {
		$constants = self::getConstants();
		if ($strict)
			return array_key_exists($name, $constants);
		$keys = array_map('strtolower', array_keys($constants));
		return in_array(strtolower($name), $keys);
	}

	/**
	 * Checks if value exists in enum
	 * @param: (mixed)
	 * @return: (bool)
	 */
	public static function isValidValue($value) {
		$values = array_values(self::getConstants());
		return in_array($value, $values, $strict = true);
	}

	public static function getAllConstants(){
		return array_values(self::getConstants());
	}

	/**
	 * Returns value with a given name
	 * @param: (string)
	 * @return: (mixed)
	 */
	public static function getValueByName($name) {
		$constants = self::getConstants();
		if(array_key_exists($name, $constants))
			return $constants[$name];
		return false;
	}

	/**
	 * Returns the name of the constant with a given value
	 * If Enum has non-unqiue values then the first instance is returned
	 * Should have it return array of constants with given value
	 * @param: (string)
	 * @return: (mixed)
	 */
	public static function getNameByValue($value) {
		$constants = self::getConstants();
		$flip = array_flip($constants);
		if (array_key_exists($value, $flip))
			return $flip[$value];
		return false;
	}

	/**
	 * Gets constant from defined enum
	 * @return: (mixed)
	 */
	private static function getConstants() {
		if (self::$constCacheArray == NULL) {
			self::$constCacheArray = [];
		}
		$calledClass = get_called_class();
		if (!array_key_exists($calledClass, self::$constCacheArray)) {
			$reflect = new ReflectionClass($calledClass);
			self::$constCacheArray[$calledClass] = $reflect->getConstants();
		}
		return self::$constCacheArray[$calledClass];
	}

}
