import time
from gattlib import GATTRequester

req = GATTRequester("98:4f:ee:10:d4:90")

while True:
	data = req.read_by_uuid("3a19")
	print data
	time.sleep(0.005)
