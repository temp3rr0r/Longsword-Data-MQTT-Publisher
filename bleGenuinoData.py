import struct
import time
from gattlib import GATTRequester

req = GATTRequester("98:4f:ee:10:d4:90")

bufferSize = 4
while True:
	data = [0] * bufferSize
	for i in range(bufferSize):
		data[i] = req.read_by_uuid("3a19")[0]

	dataList = []
	for j in range(0, bufferSize):
#		for i in range(0, 6):
#			floatValue = struct.unpack_from('f', data[j], 2 * i)
#			print "Buffer {0}, {1}: {2}".format(j, i, floatValue)

#	        currentBufferMsg = '{ ax: '+ str(struct.unpack_from('f', data[j], 0)) + ', ay:' + str(struct.unpack_from('f', data[j], 2)) + 'az:' + str(struct.unpack_from('f', data[j], 4))+ ', gx:' + str(struct.unpack_from('f', data[j], 6)) + 'gy:' + str(
#		currentBufferMsg = '{ ax: '+ str(struct.unpack_from('f', data[j], 0)[0]) + ', ay:' + str(struct.unpack_from('f', data[j], 2)) + 'az:' + str(struct.unpack_from('f', data[j], 4))+ ', gx:' + str(struct.unpack_from('f', data[j], 6)) + 'gy:' + str(struct.unpack_from('f', data[j], 8)) + ', gz:' + str(struct.unpack_from('f', data[j], 10))  + '}'
#		currentBufferMsg = '{ ax: '+ str(struct.unpack_from('f', data[j], 0))[0] + ', ay:' + str(struct.unpack_from('f', data[j], 2))[0] + ', az:' + str(struct.unpack_from('f', data[j], 4))+ ', gx:' + str(struct.unpack_from('f', data[j], 6))[0] + ', gy:' + str(struct.unpack_from('f', data[j], 8))[0] + ', gz:' + str(struct.unpack_from('f', data[j], 10))  + '}'
#		currentBufferMsg = '{ ax: '+ str(struct.unpack_from('f', data[j], 0))[0] + ', ay:' + str(struct.unpack_from('f', data[j], 2))[0] + ', az:' + str(struct.unpack_from('f', data[j], 4))[0] + ', gx:' + str(struct.unpack_from('f', data[j], 6))[0] + ', gy:' + str(struct.unpack_from('f', data[j], 8))[0] + ', gz:' + str(struct.unpack_from('f', data[j], 10))[0]  + '}'

		currentBufferMsg = '{ ax: '+ str(struct.unpack_from('f', data[j], 0)[0]) + ', ay:' + str(struct.unpack_from('f', data[j], 2)[0]) + ', az:' + str(struct.unpack_from('f', data[j], 4)[0]) + ', gx:' + str(struct.unpack_from('f', data[j], 6)[0]) + ', gy:' + str(struct.unpack_from('f', data[j], 8)[0]) + ', gz:' + str(struct.unpack_from('f', data[j], 10)[0])  + '}'
                dataList.append(currentBufferMsg)


	time.sleep(1.05)

	print dataList[0]
