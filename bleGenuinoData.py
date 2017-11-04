import json
import struct
import time
from gattlib import GATTRequester

req = GATTRequester("98:4f:ee:10:d4:90")

bufferSize = 4

class ImuPacket(): pass

while True:
	data = [0] * bufferSize
	for i in range(bufferSize):
		data[i] = req.read_by_uuid("3a19")[0]

	dataList = []
	imuPacketList = []
	for j in range(0, bufferSize):

		currentBufferMsg = '{ ax: '+ str(struct.unpack_from('f', data[j], 0)[0]) + ', ay:' + str(struct.unpack_from('f', data[j], 2)[0]) + ', az:' + str(struct.unpack_from('f', data[j], 4)[0]) + ', gx:' + str(struct.unpack_from('f', data[j], 6)[0]) + ', gy:' + str(struct.unpack_from('f', data[j], 8)[0]) + ', gz:' + str(struct.unpack_from('f', data[j], 10)[0])  + '}'
		
		currentImuPacket = ImuPacket()
		currentImuPacket.ax = struct.unpack_from('f', data[j], 0)[0]
                currentImuPacket.ay = struct.unpack_from('f', data[j], 2)[0]
                currentImuPacket.az = struct.unpack_from('f', data[j], 4)[0]
                currentImuPacket.gx = struct.unpack_from('f', data[j], 6)[0]
                currentImuPacket.gy = struct.unpack_from('f', data[j], 8)[0]
                currentImuPacket.gz = struct.unpack_from('f', data[j], 10)[0]
		currentImuPacket.timestamp = time.time()


		imuPacketList.append(currentImuPacket)

                dataList.append([0, currentBufferMsg])


	dataListStr = json.dumps(dataList) # '[1, 2, [3, 4]]'
	print dataListStr
	print ""


	class C(): pass
	class D(): pass
	c = C()
	c.what = "now?"
	c.now = "what?"
	c.d = D()
	c.d.what = "d.what"	
	classesStr = json.dumps(c, default=lambda o: o.__dict__)
	print classesStr

	imuPacketListStr = json.dumps(imuPacketList, default=lambda o: o.__dict__)
	print imuPacketListStr

	time.sleep(1.05)
