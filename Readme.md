# Data generator

My generator for random data in specified format. Works with multiple threads. Generates up to 1TB data less than in hour.
It creates as many separate files as many threads you specified.

## Create config file:

json (dict) with keys = column names, values = types

types:
1. randstr - random string (lenght = random(2, 10))

2. randint - random int:
- randint - random int (random(0, INT64_MAX))
- randint(n) - random int with len = n
- randint(a,b) - random int (random(a,b))

3. filename - random element from file with filename


## Execute gen_data.py

For help use
python gen_data.py -h
