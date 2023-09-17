The `formatTime()` function formats times using a subset of the [Java Formatter pattern](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/util/Formatter.html#dt) format. The following formats are supported:

|Symbol|Description|Example|
|---|---|---|
|`%H`|Hour of the day for the 24-hour clock, formatted as two digits with a leading zero as necessary.|00, 23|
|`%I`|Hour for the 12-hour clock, formatted as two digits with a leading zero as necessary.|01, 12|
|`%k`|Hour of the day for the 24-hour clock.|0, 23|
|`%l`|Hour for the 12-hour clock.|1, 12|
|`%M`|Minute within the hour formatted as two digits with a leading zero as necessary.|00, 59|
|`%S`|Seconds within the minute, formatted as two digits with a leading zero as necessary.|00, 60 (leap second)|
|`%L`|Millisecond within the second formatted as three digits with leading zeros as necessary.|000 - 999|
|`%N`|Nanosecond within the second, formatted as nine digits with leading zeros as necessary.|000000000 - 999999999|
|`%p`|Locale-specific morning or afternoon marker in lower case.|am, pm|
|`%z`|RFC 822 style numeric time zone offset from GMT.|-0800|
|`%Z`|A string representing the abbreviation for the time zone.|UTC, EAT|
|`%s`|Seconds since the beginning of the epoch starting at 1 January 1970 00:00:00 UTC (UNIXTIME)|1674304923|
|`%Q`|Milliseconds since the beginning of the epoch starting at 1 January 1970 00:00:00 UTC|1674304923001.|
|`%B`|Locale-specific full month name.|"January", "February"|
|`%b`|Locale-specific abbreviated month name.|"Jan", "Feb"|
|`%h`|Same as 'b'.|"Jan", "Feb"|
|`%A`|Locale-specific full name of the day of the week.|"Sunday", "Monday"|
|`%a`|Locale-specific short name of the day of the week.|"Sun", "Mon".|
|`%C`|Four-digit year divided by 100, formatted as two digits with leading zero as necessary|00, 99|
|`%Y`|Year, formatted as at least four digits with leading zeros as necessary.|0092, 2023|
|`%y`|Last two digits of the year, formatted with leading zeros as necessary.|00, 23|
|`%j`|Day of year, formatted as three digits with leading zeros as necessary.|001 - 366|
|`%m`|Month, formatted as two digits with leading zeros as necessary.|01 - 13|
|`%d`|Day of month, formatted as two digits with leading zeros as necessary.|01 - 31|
|`%e`|Day of month, formatted as two digits.|1 - 31|
|`%R`|Time formatted as "%H:%M".|23:59|
|`%T`|Time formatted as "%H:%M:%S".|23:59:59|
|`%r`|Time formatted as "%I:%M:%S %p". NOTE: AM and PM will be uppercase unlike for %p.|01:21:11 PM|
|`%D`|Date formatted as "%m/%d/%y".|01/31/23|
|`%F`|ISO 8601 complete date formatted as "%Y-%m-%d"|1989-06-04|
|`%c`|Date and time formatted as "%a %b %d %T %Z %Y"|Thu Feb 02 11:03:28 Z 2023|

```
| formatTime(format="%Y-%m-%d %H:%M:%S.L", field=firstLogon, as="firstLogon")
```

[formatTime Documentation](https://library.humio.com/data-analysis/functions-formattime.html)
