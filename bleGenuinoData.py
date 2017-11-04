import struct
import time
from gattlib import GATTRequester

req = GATTRequester("98:4f:ee:10:d4:90")

bufferSize = 1
while True:
	data = [0] * bufferSize
	for i in range(bufferSize):
		data[i] = req.read_by_uuid("3a19")[0]

	print "data"
	print str(data)
	print ""

	print "data[0]"
	print str(data[0])
	print ""

	print "data[0][0]"
	print str(data[0][0])
	print ""	


	for i in range(0, 6):
		floatValue = struct.unpack_from('f', data[0], 2 * i)
		print "float {0}: {1}".format(i, floatValue)

        print("bytes received:")
       # for b in data[0]:
        #    print str(b)
        #    print ", "
        #    #print ord(b)
        #    print ", "
        #print("")

	time.sleep(1.05)
