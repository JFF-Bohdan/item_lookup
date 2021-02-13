# Item lookup

Repository for education purpose. Code for blog post (link will be added after 
article will be ready for publishing).

As data file we will use file with expired passports from Russia, this file 
can be downloaded [here](http://сервисы.гувм.мвд.рф/info-service.htm?sid=2000)
Just use big link in the middle of the page.

## Initialization

Please create virtual environment and activate it. To find more information how to do this,
please use [this article](https://docs.python.org/3/tutorial/venv.html)

Install all dependencies using:

```
pip install -r requirements-dev.txt
```

For Linux OS you will need to use `pip3` instead of `pip`

## Implementations

### Linear search

Just basic linear search that able to scan file line by line and check if
required record exists or not.

The application can be started like:

```
python linear_search.py --input-file e:/tmp/ru_passports/list_of_expired_passports.csv
```

assuming that file was downloaded to `e:/tmp/ru_passports/list_of_expired_passports.csv`

Example output:

```
2021-02-13 15:42:32.121 | INFO     | __main__:main:33 - Application started
2021-02-13 15:42:32.123 | DEBUG    | __main__:main:36 - args: Namespace(input_file='e:/tmp/ru_passports/list_of_expired_passports.csv')
Passport series: 8003
Passport series: 409451
2021-02-13 15:42:43.652 | INFO     | __main__:main:55 - Lookup time 0.268 ms (267700 ns). Is passport expired: True
Passport series: 0104
Passport series: 167806
2021-02-13 15:43:34.713 | INFO     | __main__:main:55 - Lookup time 32636.131 ms (32636131400 ns). Is passport expired: True
Passport series: 6009
Passport series: 699906
2021-02-13 15:44:54.580 | INFO     | __main__:main:55 - Lookup time 70153.136 ms (70153136100 ns). Is passport expired: True
Passport series: 1234
Passport series: 567890
2021-02-13 15:46:14.039 | INFO     | __main__:main:55 - Lookup time 73625.309 ms (73625308900 ns). Is passport expired: False
```

It was tested with four inputs:

- `8003,409451` - from the beginning of the file
- `0104,167806` - somewhere in the middle of the file
- `6009,699906` - at the end of the file
- `1234,567890` - not available in the file
