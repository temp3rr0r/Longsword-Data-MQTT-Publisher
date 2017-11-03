import time
from gattlib import GATTRequester
import numpy as np

req = GATTRequester("98:4f:ee:10:d4:90")

bufferSize = 10
while True:
	data = [0] * bufferSize
	for i in range(bufferSize):
		data[i] = req.read_by_uuid("3a19")
	print data
	time.sleep(0.05)
