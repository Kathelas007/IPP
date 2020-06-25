# BasicEnum-PHP
Mimics enumeration with extendable class

## Usage
```php
// Also consider making final instead of abstract
abstract class DaysOfWeek extends BasicEnum {
    const Sunday = 0;
    const Monday = 1;
    const Tuesday = 2;
    const Wednesday = 3;
    const Thursday = 4;
    const Friday = 5;
    const Saturday = 6;
}

// Validating names
DaysOfWeek::isValidName('Humpday');                  // false
DaysOfWeek::isValidName('Monday');                   // true
DaysOfWeek::isValidName('monday');                   // true
DaysOfWeek::isValidName('monday', $strict = true);   // false
DaysOfWeek::isValidName(0);                          // false

// Validating values
DaysOfWeek::isValidValue(0);                         // true
DaysOfWeek::isValidValue(5);                         // true
DaysOfWeek::isValidValue(7);                         // false
DaysOfWeek::isValidValue('Friday');                  // false

// Retrieving values by name 
DaysOfWeek::getValueByName('Friday');                // 5

// Retrieving name by value -- currently assumes unique values
DaysOfWeek::getNameByValue(5);                       // Friday

// Direct reference of name
DaysOfWeek::Friday                                   // 5

```
## Credit
Examples and code should be credited to Brian Cline and others. Orignal thread can be seen at the link below
http://stackoverflow.com/questions/254514/php-and-enumerations
