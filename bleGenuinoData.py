import struct
import time
from gattlib import GATTRequester

req = GATTRequester("98:4f:ee:10:d4:90")

bufferSize = 4
while True:
	data = [0] * bufferSize
	for i in range(bufferSize):
		data[i] = req.read_by_uuid("3a19")[0]

	for j in range(0, bufferSize):
		for i in range(0, 6):
			floatValue = struct.unpack_from('f', data[j], 2 * i)
			print "Buffer {0}, {1}: {2}".format(j, i, floatValue)

	time.sleep(1.05)
