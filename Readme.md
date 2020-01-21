
# Create config file:

json (dict) with keys = column names, values = types

types:
1. randstr - random string (lenght = random(2, 10))

2. randint - random int:
- randint - random int (random(0, INT64_MAX))
- randint(n) - random int with len = n
- randint(a,b) - random int (random(a,b))

3. filename - random element from file with filename
