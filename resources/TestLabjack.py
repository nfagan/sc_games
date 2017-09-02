import sys
from datetime import datetime
from time import sleep
import u3


# make sure Exodriver (from Labjack website) and the U3 package are installed before using
fio_num = 5

try:
	d = u3.U3()
except:
	print "Error: Unable to interface with the Labjack device. Are you sure it's properly connected to this computer?"
	sys.exit()

d.getCalibrationData()
timestamp = str(datetime.now())
d.setFIOState(fio_num, state=1)
print "Set FIOS%d to \"high\" at %s." % (fio_num, timestamp)
sleep(1)
print "Waiting..."
sleep(2)
timestamp = str(datetime.now())
d.setFIOState(fio_num, state=0)
print "Set FIOS%d to \"low\" (off) at %s." % (fio_num, timestamp)

