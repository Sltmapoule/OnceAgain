from scipy.signal import tf2sos

B = [1, 0, 0, 0, 0, 1]
A = [1, 0, 0, 0, 0, .9]
sos = tf2sos(B, A)
print(sos)

