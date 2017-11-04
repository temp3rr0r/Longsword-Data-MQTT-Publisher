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
logger.setLevel(logging.DEBUG)
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
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback) # TODO: proper AWS topic
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
publishDelay = 1 # seconds TODO: better delay
bufferSize = 4 # 4 packets x 24 bytes per packet (6 x float32)
class ImuPacket(): pass # Stores imu packet: timestamp and payload
class ImuPayload(): pass # Stores imu data

try:
	req = GATTRequester("98:4f:ee:10:d4:90") # BLE genuino 101 address

	while True:
		data = [0] * bufferSize # Init buffer	        

	        for i in range(bufferSize):
        	        data[i] = req.read_by_uuid("3a19")[0] # Read IMU data

		imuPacketList = []
		for j in range(0, bufferSize): # TODO: should i merge this and the previous loop?

	                currentImuPayload = ImuPayload()
	                currentImuPayload.ax = round(struct.unpack_from('f', data[j], 0)[0], 2)
	                currentImuPayload.ay = round(struct.unpack_from('f', data[j], 2)[0], 2)
	                currentImuPayload.az = round(struct.unpack_from('f', data[j], 4)[0], 2)
	                currentImuPayload.gx = round(struct.unpack_from('f', data[j], 6)[0], 2)
	                currentImuPayload.gy = round(struct.unpack_from('f', data[j], 8)[0], 2)
        	        currentImuPayload.gz = round(struct.unpack_from('f', data[j], 10)[0], 2)
 
			currentImuPacket = ImuPacket()
                	currentImuPacket.timestamp = round(time.time(), 3)
	                currentImuPacket.data = currentImuPayload								

        	        imuPacketList.append(currentImuPacket)			

		msg = json.dumps(imuPacketList, default=lambda o: o.__dict__)
		#print msg

		myAWSIoTMQTTClient.publish(topic, msg, 1)
		loopCount += 1
		time.sleep(publishDelay)

except KeyboardInterrupt:
	pass

print('Exiting the loop');
myAWSIoTMQTTClient.disconnect()
print('Disconnected from AWS')
