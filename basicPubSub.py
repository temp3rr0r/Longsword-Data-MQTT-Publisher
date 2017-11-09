import csv
import json
import struct
from gattlib import GATTRequester
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Read in command-line parameters
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--endpoint", action="store", required=True, dest="host", help="Your AWS IoT custom endpoint")
parser.add_argument("-r", "--rootCA", action="store", required=True, dest="rootCAPath", help="Root CA file path")
parser.add_argument("-c", "--cert", action="store", dest="certificatePath", help="Certificate file path")
parser.add_argument("-k", "--key", action="store", dest="privateKeyPath", help="Private key file path")
parser.add_argument("-w", "--websocket", action="store_true", dest="useWebsocket", default=False,
                    help="Use MQTT over WebSocket")
parser.add_argument("-id", "--clientId", action="store", dest="clientId", default="basicPubSub",
                    help="Targeted client id")
parser.add_argument("-t", "--topic", action="store", dest="topic", default="sdk/test/Python", help="Targeted topic")

args = parser.parse_args()
host = args.host
rootCAPath = args.rootCAPath
certificatePath = args.certificatePath
privateKeyPath = args.privateKeyPath
useWebsocket = args.useWebsocket
clientId = args.clientId
topic = args.topic

if args.useWebsocket and args.certificatePath and args.privateKeyPath:
    parser.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not args.useWebsocket and (not args.certificatePath or not args.privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.ERROR)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
#myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
publishDelay = 0.010 # seconds TODO: better delay
bufferSize = 1 # 4 packets x 20 bytes per packet MAX (5 x int32)
class ImuPacket(): pass # Stores imu packet: timestamp and payload
class ImuPayload(): pass # Stores imu data

while True:
	try:
		req = GATTRequester("98:4f:ee:10:d4:90") # BLE genuino 101 address

		while True:			
			data = [[] for i in range(20)] # Accelerometer buffer
			data2 = [[] for i in range(20)] # Magnetometer buffer

	        	for i in range(bufferSize): # Read IMU data
	        	        data[i] = req.read_by_uuid("3a19")[0]
				data2[i] = req.read_by_uuid("3a20")[0]

			imuPacketList = []
			for j in range(0, bufferSize): # TODO: should i merge this and the previous loop?

		                currentImuPayload = ImuPayload()
	        	        currentImuPayload.ax = struct.unpack_from('i', data[j], 0)[0]
		                currentImuPayload.ay = struct.unpack_from('i', data[j], 4)[0]
		                currentImuPayload.az = struct.unpack_from('i', data[j], 8)[0]

		                currentImuPayload.gx = struct.unpack_from('i', data2[j], 0)[0]
		                currentImuPayload.gy = struct.unpack_from('i', data2[j], 4)[0]
	        	        currentImuPayload.gz = struct.unpack_from('i', data2[j], 8)[0]

				currentImuPayload.classification = 3 # Current gesture class

				currentImuPacket = ImuPacket()
	                	currentImuPacket.timestamp = round(time.time(), 3)
		                currentImuPacket.data = currentImuPayload
        		        imuPacketList.append(currentImuPacket)

				#with open('longsword.csv', 'a') as csvfile:
				#        csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				        #csvWriter.writerow(['classification','ax', 'ay', 'az', 'gx', 'gy', 'gz'])
				#	csvWriter.writerow([currentImuPayload.classification, currentImuPayload.ax, currentImuPayload.ay, currentImuPayload.az, currentImuPayload.gx, currentImuPayload.gy, currentImuPayload.gz])

			msg = json.dumps(imuPacketList[0], default=lambda o: o.__dict__)
			#print msg
			myAWSIoTMQTTClient.publish(topic, msg, 1) # Publish to DynamoDB via IoT
			loopCount += 1
			time.sleep(publishDelay)

	except:
		print "Exception. Retrying.."
		time.sleep(2)
		#pass

print('Exiting the loop');
myAWSIoTMQTTClient.disconnect()
print('Disconnected from AWS')
