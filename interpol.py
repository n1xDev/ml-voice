import numpy
from scipy.interpolate import interp1d

def Main():
	arr = []
	
	arr.append(200)
	arr.append(190)
	arr.append(360)
	arr.append(340)
	arr.append(370)
	arr.append(425)
	arr.append(357)
	arr.append(367)
	print(arr)
	new_arr = [None] * 10
	ExpendArr(new_arr, len(new_arr), arr, len(arr))

def ExpendArr(out, out_len, source, source_len):
	k = float((float(out_len) - 1.0) / float(source_len - 1.0))
	i = 1
	while i < out_len - 1:
		i1 = int(i/k)
		frac = float(float(i)/float(k) - float(i1))
		out[i] = float(float(source[i1]) * (1.0 - frac) + float(source[i1+1]) * frac)
		print(out[i])
		i += 1
	out[0] = source[0]
	print(out)
	out[out_len - 1] = source[source_len - 1]
	return out


Main()