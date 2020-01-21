
# Create config file:

json (dict) with keys = column names, values = types

types:
1) randstr - random string (lenght = random(2, 10))
2) randint - random int:
2.1) randint - random int (random(0, INT64_MAX))
2.2) randint(n) - random int with len = n
2.3) randint(a,b) - random int (random(a,b))
3) filename - random element from file with filename
