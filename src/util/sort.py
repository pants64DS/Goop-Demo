from functools import cmp_to_key

def lessthan_to_3waycmp(lt, a, b):
	if lt(a, b):
		return -1
	if lt(b, a):
		return 1

	return 0

def sort(c, lt):
	c.sort(key=cmp_to_key(lambda a, b: lessthan_to_3waycmp(lt, a, b)))
