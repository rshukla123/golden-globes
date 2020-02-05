
# arr is the list of tokens, n is the length of n-gram
def ngrams(arr, n):
	return [arr[i:i+n] for i in range(len(arr)-n+1)]

def prog_print(i, size, width=20):
	prog = round((i / size) * width)
	print('\r|' + prog * '=' + (width - prog) * ' ' + '|', end='')
	if i == size:
		print('\r|' + width*'=' + '|')