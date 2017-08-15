from psychopy.hardware.labjacks import U3
from datetime import datetime

# alter addresses and ranges until triggers are sent reliably
# make sure Exodriver (from Labjack website) and the U3 package are installed before using

device = U3()
for address in (6700, 6701, 6702):
	for value in range(0, 256):
		timestamp = str(datetime.now())
		print "Sending value %s over address %s at %s" % (value, address, timestamp)
		device.setData(value, address = address)