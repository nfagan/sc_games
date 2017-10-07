import sys
from datetime import datetime
from time import sleep
import u3

try:
	fio_num = int(sys.argv[1])
	assert fio_num in (4, 5, 6, 7)
except:
	print "This script tests Labjack FIO ports 4-7"
	print "Usage: python %s 4 (or 5-7)" % __file__
	sys.exit()

# make sure Exodriver (from Labjack website) and the U3 package are installed before using
try:
	d = u3.U3()
except:
	print "Error: Unable to interface with the Labjack device. Are you sure it's properly connected to this computer?"
	sys.exit()

d.getCalibrationData()
timestamp = str(datetime.now())
d.setFIOState(fio_num, state=1)
print "Set FIO%d to \"high\" at %s." % (fio_num, timestamp)
sleep(1)
print "Waiting..."
sleep(2)
timestamp = str(datetime.now())
d.setFIOState(fio_num, state=0)
print "Set FIO%d to \"low\" (off) at %s." % (fio_num, timestamp)

